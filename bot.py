from typing import Union
from discord.ext.commands.core import check
import jury
import discord
from discord import Embed
from discord.ext import commands

TOKEN = "YOUR_TOKEN_HERE"
# Don't use my token, use yours!

bot = commands.Bot(command_prefix="$", case_insensitive=True)

def check_valid_question_number_string(content: str) -> bool:
    content = content.lstrip("q")
    return content.isdigit() and 0 < int(content) <= len(jury.questions)

def check_valid_question_number_message(message: discord.Message) -> bool:
    return check_valid_question_number_string(message.content)

def check_valid_language_string(content: str) -> bool:
    return content in ("cpp", "c++", "py", "python")

def check_valid_language_message(message: discord.Message) -> bool:
    return check_valid_language_string(message.content)

def check_valid_codeblock_string(content: str) -> bool:
    lines = content.split("\n")
    is_codeblock = lines[0].startswith("```")
    if is_codeblock:
        return (" " not in lines[0]) and (lines[-1] == "```")
    else:
        return not lines[0].startswith("```") or lines[-1].endswith("```")

def check_valid_codeblock_message(message: discord.Message) -> bool:
    return check_valid_codeblock_string(message.content)

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))

@bot.command()
async def summary(ctx: commands.Context) -> None:
    '''Lists user's submissions and their recorded times.
    '''
    message = ""
    user_id = ctx.message.author.id
    total_time = 0
    for q_no in range(len(jury.questions)):
        question = jury.questions[q_no]
        if question['level'] != jury.questions[q_no-1]['level']:
            message += f"\n\n**{question['level']}:**\n*Non-submission multiplier = x{question['multiplier']}*"
        message += f"\nQ{q_no+1}. {question['name']}: "  # -1 for 0 indexed
        judgement = jury.get_judgement(user_id, q_no)
        if judgement:
            message += f"{judgement.time_taken} ms"
            total_time += judgement.time_taken
        else:
            message += f" Not submitted"
    message += f"\n\n\n**Total time** (w/o penalties): {total_time} ms"
    await ctx.message.channel.send(message)
            
@bot.command()
async def leaderboard(ctx: commands.Context) -> None:
    '''Shows a true leaderboard (penalty-aware) of the participants
    '''
    leaderboard = jury.get_leaderboard()
    message = ""
    if len(leaderboard) == 0:
        await ctx.channel.send("No submissions yet.")
    else:
        for rank in range(len(leaderboard)):
            p_data = leaderboard[rank]
            message = "\n"
            if rank == 0:
                message += "🥇"
            elif rank == 2:
                message += "🥈"
            elif rank == 3:
                message += "🥉"
            else:
                message = f"  {rank+1}."
            message += "  "  # Arbitrary padding
            message += f"<@{p_data['id']}>: {p_data['time']}ms"
        await ctx.channel.send(message)

@bot.command()
async def diff(ctx: commands.Context, question_number: str=None) -> None:
    '''Shows a unified diff between output and answer for a submitted question.

    Args:
        question_number: The question to view the diff for. Defaults to the last submitted question.
    '''
    if not check_valid_question_number_string(question_number):
        question_number = await bot.wait_for("message", check=check_valid_question_number_message)
        question_number = question_number.content
    question_number = int(question_number.lower().lstrip("q"))
    # Change question number to 0 indexed
    question_number -= 1
    judgement = jury.get_judgement(ctx.message.author.id, question_number)
    if not judgement:
        await ctx.channel.send(f"No submission found for question {question_number + 1} ({jury.questions[question_number]['name']}).")  # Back to 1 indexed
    else:
        await ctx.channel.send(f"Diff\n```diff\n{judgement.diff.unified}\n```") 

@bot.command()
async def submit(ctx: commands.Context, question_number: str=None, language: str=None) -> None:
    f'''Initiates a prompt to submit code for a question.
    
    Args:
        question_number: A valid question number. Expected format: q1, 2, q3, etc.
        language: The language the submission is in. Must be either "cpp", "c++", "py" or "python".
    '''
    if question_number is None or not check_valid_question_number_string(question_number):
        await ctx.channel.send("What question are you submitting? (q1, 2, q3, etc.)")
        question_number = await bot.wait_for("message", check=check_valid_question_number_message)
        question_number = question_number.content
    question_number = int(question_number.lstrip('q'))

    if language is None or not check_valid_language_string(language):
        await ctx.channel.send("What language is your submission in? (\"cpp\", \"c++\", \"py\", \"python\".)")
        language = await bot.wait_for("message", check=check_valid_language_message)
        language = language.content
    language = "cpp-clang" if language.lower() in ("c++", "cpp") else "python3"

    
    await ctx.channel.send(f'''Enter your code for Q{question_number} {jury.questions[question_number-1]['name']} (to be run on {language}).
Send your code in a codeblock:
Input:
\```
print("Hello, World!")
\```
Output:
```
print("Hello, World!")
```
Do not keep your code and the backticks on the same line.''')
    code = await bot.wait_for("message", check=check_valid_codeblock_message)
    code = code.content
    source_lines = code.split("\n")
    if code.startswith("```"):
        source_lines = source_lines[1:-1]  # Remove codeblock markdown
    source_code = "\n".join(source_lines)

    # Change question to 0 indexed
    question_number -= 1
    await ctx.channel.send("Your code is being judged.")

    async with ctx.typing():
        judgement = jury.judge(question_number, language, source_code)
        # OUTPUT
        message = ""
        if judgement.passed:
            message += "All Correct \✔️"
            message += f"\n\n**Time Considered:** {float(judgement.time_taken)} ms"
        else:   
            message += f"\❌ Wrong Answer on line {judgement.diff.flod}"  # First line of difference
            message += f"\n\nInput\n```\n{judgement.question['input']}\n```"
            message += f"\n\nOutput\n```\n{judgement.output}\n```"
            message += f"\n\nAnswer\n```\n{judgement.question['answer']}\n```"
            message += f"\n\n**Time Considered:** N.A."
            message += f"\nUse the `$diff question_number` command to view a unified view of the output and the answer."

        jury.log(ctx.message.author.id, judgement)
        await ctx.channel.send(message)
        
@bot.command()
async def view(ctx: commands.Context, question_number: str) -> None:
    '''Displays the given question.
    '''
    if not check_valid_question_number_string(question_number):
        await ctx.channel.send("What question do you want to view? (q1, 2, q3, etc.)")
        question_number = await bot.wait_for("message", check=check_valid_question_number_message)
        question_number = question_number.content
    question_number = int(question_number.lstrip('q'))
    question = jury.questions[question_number-1]
    question_prompt = question["question"]
    question_prompt = f"**Q{question_number}. {question['name']}**\n" + question_prompt
    await ctx.channel.send(question_prompt)

bot.run(TOKEN)