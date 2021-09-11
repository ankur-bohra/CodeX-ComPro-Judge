import discord
from brainfuck import Tio
import re
client = discord.Client()
site = Tio()
einput = {
    "q1": "12 “green” 548.67 “Codex” “156” 23",
    "q2": "100 200",
    "q3": """5 1\n1 2 3 4 1"""
}

eoutput = {
    "q2" : "300",
    "q1" : "['“green”', '12', '“Codex”', '548.67', '23', '“156”']",
    "q3" : "5" 
}
def judge(code, lang, input):
    code = code.content
    code = code.replace("```", "")
    request = site.new_request(lang, code.lstrip(), inputs=input)
    output = site.send(request)
    return output

def passfail(result, output):
    if result.count(output) > 0:
        return "```Test Case Passed ✔️```"
    else:
        return "```Test Case Failed ❌```" + "```Expected Output: {0}```".format(output)
# score = 0
@client.event
async def on_ready():
    print('you have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # global score
    if message.author == client.user:
        return
    
    def qnum(m):
        return m.author == message.author and m.content.startswith(">q")
    
    def codecheck(m):
        return m.author == message.author and m.content.startswith("```")
    
    def langcheck(m):
        return m.author == message.author
    
    if message.content.startswith('>whoami'):
        await message.channel.send('C0D3X BOT')
    elif message.content.startswith(">help"):
        f = open('help.md', 'r')
        r = f.read()
        await message.channel.send("```\n" + r + "\n```")

    elif message.content.startswith(">submit"):
        await message.channel.send("What question number do you want to submit?")
        #add filter for question number
        try:
            msg = await client.wait_for("message", check=qnum, timeout=10.0)
        except:
            await message.channel.send("timeout")

        if msg.content.startswith(">q1"):
            try:
                await message.channel.send("what language are you using?")
                lang = await client.wait_for("message", check=langcheck, timeout=10.0)
                if lang.content.startswith(">python"):
                    await message.channel.send("write your python code here")
                    code = await client.wait_for("message", check=codecheck)
                    output = judge(code, "python3", einput["q1"])
                    await message.channel.send(output)
                    pass_or_fail = passfail(output, eoutput["q1"])
                    # if pass_or_fail == "```Test Case Passed ✔️```":
                    #     score = score + 1
                    await message.channel.send(pass_or_fail)

                elif lang.content.startswith(">cpp"):
                    await message.channel.send("write your c++ code here")
                    code = await client.wait_for("message", check=codecheck)
                    output = judge(code, "cpp-clang", einput["q1"])
                    await message.channel.send(output)
                    pass_or_fail = passfail(output, eoutput["q1"])
                    # if pass_or_fail == "```Test Case Passed ✔️```":
                    #     score = score + 1
                    await message.channel.send(pass_or_fail)
            except Exception as e:
                await message.channel.send(e)


        if msg.content.startswith(">q2"):
            try:
                await message.channel.send("what language are you using?")
                lang = await client.wait_for("message", check=langcheck, timeout=10.0)
                if lang.content.startswith(">python"):
                    await message.channel.send("write your python code here")
                    code = await client.wait_for("message", check=codecheck)
                    output = judge(code, "python3", einput["q2"])
                    await message.channel.send(output)
                    pass_or_fail = passfail(output, eoutput["q2"])
                    # if pass_or_fail == "```Test Case Passed ✔️```":
                    #     score = score + 1
                    await message.channel.send(pass_or_fail)
                elif lang.content.startswith(">cpp"):
                    await message.channel.send("write your c++ code here")
                    code = await client.wait_for("message", check=codecheck)
                    output = judge(code, "cpp-clang", einput["q2"])
                    await message.channel.send(output)
                    pass_or_fail = passfail(output, eoutput["q2"])
                    # if pass_or_fail == "```Test Case Passed ✔️```":
                    #     score = score + 1
                    await message.channel.send(pass_or_fail)

            except Exception as e:
                await message.channel.send(e)
            

        if msg.content.startswith(">q3"):
            try:
                await message.channel.send("what language are you using?")
                lang = await client.wait_for("message", check=langcheck, timeout=10.0)
                if lang.content.startswith(">python"):
                    await message.channel.send("write your python code here")
                    code = await client.wait_for("message", check=codecheck, timeout=30.0)
                    output = judge(code, "python3", einput["q3"])
                    await message.channel.send(output)
                    pass_or_fail = passfail(output, eoutput["q3"])
                    # if pass_or_fail == "```Test Case Passed ✔️```":
                    #     score = score + 1
                    await message.channel.send(pass_or_fail)

                elif lang.content.startswith(">cpp"):
                    await message.channel.send("write your c++ code here")
                    code = await client.wait_for("message", check=codecheck)
                    output = judge(code, "cpp-clang", einput["q3"])
                    await message.channel.send(output)
                    pass_or_fail = passfail(output, eoutput["q3"])
                    # if pass_or_fail == "```Test Case Passed ✔️```":
                    #     score = score + 1
                    await message.channel.send(pass_or_fail)
            except:
                await message.channel.send("timeout")

    elif message.content.startswith(">problems"):
        f = open("questions.md", 'r', encoding="utf-8")
        rx = f.read()
        await message.channel.send("```\n" + rx + "\n```")

client.run('ODgxMTk2NzQyODU3NjA1MTQx.YSpUaw.PXDD7tuTrSVKhobhmCmVlBJNJqs')