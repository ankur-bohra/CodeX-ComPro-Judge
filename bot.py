import os
import pickle
import pytz
import shutil
from io import BytesIO
from typing import Union, IO, Dict, List
from discord.ext.commands.core import check
import jury
import discord
from discord.ext import commands

TOKEN = "ODg2MjUwMDIyNDcwMDQ1NzA2.YTy2pw.wqb5lFhu7O8GkG-YL8iAoHjB5MM"
# Don't use my token, use yours!

bot = commands.Bot(command_prefix="$", case_insensitive=True)

def check_valid_question_number_string(content: str) -> bool:
    content = content.lstrip("q")
    return content.isdigit() and 0 < int(content) <= len(jury.questions)

def check_valid_question_number_message(message: discord.Message) -> bool:
    if message.author.id == bot.user.id:
        return False
    return check_valid_question_number_string(message.content)

def check_valid_language_string(content: str) -> bool:
    return content in ("cpp", "c++", "py", "python")

def check_valid_language_message(message: discord.Message) -> bool:
    if message.author.id == bot.user.id:
        return False
    return check_valid_language_string(message.content)

def check_valid_codeblock_string(content: str) -> bool:
    lines = content.split("\n")
    is_codeblock = lines[0].startswith("```")
    if is_codeblock:
        return (" " not in lines[0]) and (lines[-1] == "```")
    else:
        return not lines[0].startswith("```") or lines[-1].endswith("```")

def check_valid_codeblock_message(message: discord.Message) -> bool:
    if message.author.id == bot.user.id:
        return False
    if len(message.attachments) == 0:
        return check_valid_codeblock_string(message.content)
    else:
        return True

def check_code_is_same(team: str, code: str, question_number: int) -> bool:
    judgement = jury.get_judgement(team, question_number)
    return judgement and judgement["code"].strip() == code.strip()

def get_identifier(user) -> str:
    roles = user.roles
    identifier = ""
    for role in roles:
        if role.name.lower() in ('lotus valley', 'dav public school', 'heritage school', 'gd goenka', 'shalom hills', 'kunskapsskolan', 'dps'):
            identifier = role.name
            break
    else:
        identifier = str(user.id)
    return identifier

format_time = lambda object: object.strftime('%I:%M:%S %p')

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))

@bot.command()
async def summary(ctx: commands.Context) -> None:
    '''Lists user's submissions and their recorded points.
    '''
    embed = discord.Embed(title=f"{get_identifier(ctx.author)} Summary", description="These points include penalties, and may change with time.", color=0xc0c0c0)
    questions_string = ""
    points_string = ""
    total_points = 0
    for q_no in range(len(jury.questions)):
        question = jury.questions[q_no]
        judgement = jury.get_judgement(get_identifier(ctx.message.author), q_no)
        if not (judgement and judgement["passed"]):
            points = jury.get_penalised_points(q_no)
        else:
            points = judgement["points"]
        points = round(points, 2)
        questions_string += f"\nQ{q_no+1}. {question['name']}"
        points_string += f"\n{points} points"  # +1 to convert to 1 indexed
        if judgement and judgement["passed"]:
            formatted_time = format_time(judgement["submission_time"])
            points_string += f" ({judgement['execution_time']}ms @ {formatted_time})"
        else:
            points_string += f" (penalised)"
        total_points += points

    embed.add_field(name="Question", value=questions_string, inline=True)
    embed.add_field(name="Points", value=points_string, inline=True)
    embed.add_field(name="Total points", value=str(total_points) + " points", inline=False)
    embed.set_footer(
            text="Requested by " + ctx.author.display_name + " (" + get_identifier(ctx.author) + ")", icon_url = ctx.author.avatar_url)
    await ctx.message.channel.send(embed=embed)
            
@bot.command()
async def leaderboard(ctx: commands.Context) -> None:
    '''Shows a true leaderboard (penalty-aware) of the participants
    '''
    leaderboard = jury.get_leaderboard()
    if len(leaderboard) == 0:
        await ctx.channel.send("No submissions yet.")
    else:
        message = ""
        for rank in range(len(leaderboard)):
            message += "\n"
            if rank == 0:
                message += "🥇"
            elif rank == 1:
                message += "🥈"
            elif rank == 2:
                message += "🥉"
            else:
                message += f"  {rank+1}."
            t = leaderboard[rank]
            message += "  "  # Some padding
            message += f"{t['team'] + (' **(You)**' if t['team'] == get_identifier(ctx.message.author) else '')}: {t['points']} points"

        embed = discord.Embed(title="Leaderboard", description=message, color=0x3ad5eb)
        embed.set_footer(
            text="Requested by " + ctx.author.display_name + " (" + get_identifier(ctx.author) + ")", icon_url = ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

@bot.command()
async def submit(ctx: commands.Context, question_number: str=None, language: str=None, *, code: Union[str, IO]=None) -> None:
    f'''Initiates a prompt to submit code for a question.
    
    Args:
        question_number: A valid question number. Expected format: q1, 2, q3, etc.
        language: The language the submission is in. Must be either "cpp", "c++", "py" or "python".
        code: The content of the code or a file for the submission.
    '''
    # QUESTION NUMBER
    if question_number is None or not check_valid_question_number_string(question_number):
        await ctx.channel.send("What question are you submitting? (q1, 2, q3, etc.)")
        question_number = await bot.wait_for("message", check=check_valid_question_number_message)
        question_number = question_number.content
    question_number = int(question_number.lstrip('q'))

    # PROGRAMMING LANGUAGE
    if language is None or not check_valid_language_string(language):
        await ctx.channel.send("What language is your submission in? (\"cpp\", \"c++\", \"py\", \"python\".)")
        language = await bot.wait_for("message", check=check_valid_language_message)
        language = language.content
    language = "cpp-clang" if language.lower() in ("c++", "cpp") else "python3"
    
    # CODE

    if len(ctx.message.attachments) == 0 and (not code or not check_valid_codeblock_string(code)) :
        await ctx.channel.send(f'''Enter your code for Q{question_number} {jury.questions[question_number-1]['name']} (to be run on {language}).
Send your code in a codeblock (remember to keep the backticks on a separate line):
Input:
\```
print("Hello, World!")
\```
Output:
```
print("Hello, World!")
```
OR upload your file.''')
        code = await bot.wait_for("message", check=check_valid_codeblock_message)
        print(str(code))
        if len(code.attachments) == 0:
            code = code.content
        else:
            try:
                code = await code.attachments.pop().read().decode("cp1250")
            except e:
                await ctx.channel.send(f"Whoa! The bot ran into an error: Unable to read file content: {e}, please try again.")
                return
    elif len(ctx.message.attachments) > 0:
        try:
            code = await ctx.message.attachments.pop().read()
            code = code.decode("cp1250")
        except BaseException as e:
            await ctx.channel.send(f"Whoa! The bot ran into an error: Unable to read file content: {e}, please try again.")
            return

    if check_code_is_same(get_identifier(ctx.message.author), code, question_number):
        await ctx.channel.send(f"You have already submitted this same code. Please do not add unnecessary load on the bot.")
        return
    source_lines = code.split("\n")
    if code.startswith("```"):
        source_lines = source_lines[1:-1]  # Remove codeblock markdown
    source_code = "\n".join(source_lines)

    # Change question to 0 indexed
    question_number -= 1
    judgement_message = await ctx.channel.send("Your code is being judged.")

    submission_time = ctx.message.created_at
    # Tell the naive object that it's utc
    submission_time = submission_time.replace(tzinfo=pytz.timezone("UTC"))
    # Convert it to ist
    submission_time = submission_time.astimezone(pytz.timezone('Asia/Kolkata'))
    judgement = jury.judge(question_number, language, source_code, submission_time)
    jury.log(get_identifier(ctx.message.author), judgement)
    # OUTPUT
    question_string = f"Q{question_number+1}. {jury.questions[judgement['question_number']]['name']}"
    if judgement["passed"]:
        embed = discord.Embed(color=0x14b90b)
        embed.set_author(name="All Correct ✅")
        embed.add_field(name="Execution Time", value=str(judgement["execution_time"]) + " ms", inline=True)
        embed.add_field(name="Submission Time", value=format_time(judgement["submission_time"]), inline=True)
        embed.add_field(name="Submission Points", value=judgement["points"], inline=False)
    else:
        error = f"Wrong answer on line {judgement['diff']['lod']}: Expected **\"{judgement['diff']['correct']}\"**, got **\"{judgement['diff']['wrong']}\"**"
        error += f"\nUse `$tests {question_number+1}` to view this test's input, answer, and your output"
        embed = discord.Embed(color=0xf03a17, description=error)
        embed.set_author(name="Test Failed ❌")
    embed.set_footer(
            text="Requested by " + ctx.author.display_name + " (" + get_identifier(ctx.author) + ")", icon_url = ctx.author.avatar_url)
    await judgement_message.edit(content="", embed=embed)

@bot.command()
async def tests(ctx: commands.Context, question_number: str=None) -> None:
    '''Sends the given question's test input and answer
    '''
    if not question_number or not check_valid_question_number_string(question_number):
        await ctx.channel.send("What question do you want to view? (q1, 2, q3, etc.)")
        question_number = await bot.wait_for("message", check=check_valid_question_number_message)
        question_number = question_number.content
    question_number = int(question_number.lstrip('q')) - 1
    question = jury.questions[question_number]

    files = []
    question_folder_path = f"questions/{question['name']}"
    input_file = discord.File(question_folder_path + "/INPUT.txt", filename=f"Q{question_number+1} INPUT.txt")  # Display 1 indexed number
    answer_file = discord.File(question_folder_path + "/ANSWER.txt", filename=f"Q{question_number+1} ANSWER.txt")  # Display 1 indexed number
    files.extend((input_file, answer_file))

    judgement = jury.get_judgement(get_identifier(ctx.author), question_number)
    if judgement:
        output_file = BytesIO(bytes(judgement["output"], encoding="utf-8"))
        output_file = discord.File(output_file, filename=f"Q{question_number+1} {format_time(judgement['submission_time'])} OUTPUT.txt")
        files.append(output_file)

    status = "Not submitted" if not judgement else ("Passed" if judgement["passed"] else "Failed")
    message = f"Test data for question Q{question_number+1} {question['name']} ({status})"
    await ctx.channel.send(content=message, files=files)


@bot.command()
async def view(ctx: commands.Context, question_number: str=None) -> None:
    '''Displays the given question.
    '''
    if not question_number or not check_valid_question_number_string(question_number):
        await ctx.channel.send("What question do you want to view? (q1, 2, q3, etc.)")
        question_number = await bot.wait_for("message", check=check_valid_question_number_message)
        question_number = question_number.content
    question_number = int(question_number.lstrip('q'))
    question = jury.questions[question_number-1]
    question_prompt = question["question"]
    embed = discord.Embed(title=f"Q{question_number}. {question['name']}", description=question_prompt)
    embed.set_footer(
            text="Requested by " + ctx.author.display_name + " (" + get_identifier(ctx.author) + ")", icon_url = ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)


# MODERATION COMMANDS
@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def delete(ctx: commands.context, team, question_number):
    '''Deletes a team's latest submission for a certain question.

    Args:
        team: Either the team number (e.g. 1, 2) or an ID of one of the team members.
        question_number: The question number the submission is to be disqualified for.
    '''
    if len(team) > 20:
        try:
            user = ctx.message.server.get_member(int(team))
            team = get_identifier(user)
        except BaseException as e:
            ctx.channel.send(f"Couldn't find user's team: {e}")
            return

    judgement = get_judgement(team, question_number)
    if not judgement:
        ctx.channel.send(f"Team {team} has not submission for question {question_number}")
        return

    attempt_time = get_format(judgement["submission_time"])
    ctx.channel.send(f"Do you want to delete Team {team}'s submission for {question_number} at {attempt_time}?")
    message = bot.wait_for("message", check=lambda msg: msg.content.lower() in ("yes", "no"))
    if message.content.lower() == "yes":
        jury.judgements[team].pop(question_number)
        ctx.channel.send("Question judgement removed.")
    else:
        ctx.channel.send("Command cancelled.")

@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def freeze(ctx: commands.context):
    '''Freezes information about the competition into a file.
    '''
    time = ctx.message.created_at.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone('Asia/Kolkata'))
    if not os.path.exists("LOGS"):
        os.mkdir("LOGS")

    with open("LOGS/"+time.strftime("%I_%M")+".dat", "wb") as log:
        pickle.dump(jury.judgements, log)
    await ctx.channel.send("Logs dumped.")

# INITIALIZATION
@bot.listen("on_message")
async def intialize_teams(message):
    for role in message.guild.roles:
        if role.name not in jury.judgements and role.name.lower() in ('lotus valley', 'dav public school', 'heritage school', 'gd goenka', 'shalom hills', 'kunskapsskolan', 'dps'):
            jury.judgements[role.name] = {}
            print("Added", role.name)

bot.run(TOKEN)