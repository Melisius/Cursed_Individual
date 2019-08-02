import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord import File
import matplotlib.pyplot as plt
import os
import numpy as np
import asyncio


bot = commands.Bot(command_prefix='>')
bot.remove_command('help')
bot.admins = [265865052878405642,209434080385695744,264362912779337730]

bot.censor_list = []
f = open("censor_list.txt","r")
for line in f:
    bot.censor_list.append(line.strip("\n"))
f.close()
    
bot.white_list = []
f = open("white_list.txt","r")
for line in f:
    bot.white_list.append(line.strip("\n"))
f.close()

bot.mistakes_dict = {}
f = open("mistakes_dict.txt","r")
for line in f:
    if ":" in line:
        bot.mistakes_dict[line.strip("\n").split(":")[0]] = line.strip("\n").split(":")[1]
f.close()

bot.consistency_list = []
f = open("consistency_list.txt","r")
for line in f:
    bot.consistency_list.append(line.strip("\n"))
f.close()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    for word in bot.consistency_list:
        in_white_list = False
        for whiteword in bot.white_list:
            if whiteword in word:
                in_white_list = True
                break
        if not in_white_list:
            print("Not white listning:",word)
    for word in bot.white_list:
        for badword in bot.censor_list:
            if word in badword:
                print("White list overlapping with cenosr list:",word,badword)
    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("*"+ctx.message.content.split()[0]+"* is not a valid command.\nType *>help* for valid commands. "+ctx.author.mention)
        if "Direct Message" not in str(ctx.channel):
            await ctx.message.delete()
        return
    raise error


@bot.command()
async def adminhelp(ctx):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        say = "**>get_white_list**\nSends the list of partial words that will not be censored. I.e. *assa* will ensure *assault* will not be censored.\n\n"
        say += "**>add_white_list** *word*\nGive partial word to add to the white list.\n\n"
        say += "**>remove_white_list** *word*\nGive partial word to remove from the white list.\n\n"
        say += "**>get_censor_list**\nSends the list of words that will be censored. I.e. *fuck* will make *fucking* into *□□□□ing*\n\n"
        say += "**>add_censor_list** *word*\nGive word to add to the censor list.\n\n"
        say += "**>remove_censor_list** *word*\nGive word to remove from the censor list.\n\n"
        say += "**>get_mistakes_dict\n**Sends the dictionary of wrong spellings and their corrections.\n\n"
        say += "**>add_mistakes_dict** *wrong_word* *correct_word*\nAdd a wrong word spelled word and the correct spelling to the spell checker.\n\n"
        say += "**>remove_mistakes_dict** *wrong_word*\nGive a wrong word to be remove from the spell checker."
        await ctx.send(say)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()


@bot.command()
async def shutdown(ctx):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
    await ctx.bot.logout()


@bot.command()
async def get_white_list(ctx):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        say = ""
        for word in sorted(bot.white_list):
            say += word+"\n"
            if len(say) > 1900:
                await ctx.send(say)
                say = ""
        await ctx.send(say)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        
        
@bot.command()
async def add_white_list(ctx, word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        word = word.lower()
        if word not in bot.white_list:
            bot.white_list.append(word)
            f = open("white_list.txt","a")
            f.write("\n"+word)
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        
        
@bot.command()
async def remove_white_list(ctx, remove_word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        remove_word = remove_word.lower()
        if remove_word in bot.white_list:
            f = open("white_list.txt.bak","w+")
            for word in bot.white_list:
                f.write(word+"\n")
            f.close()
            bot.white_list.remove(remove_word)
            f = open("white_list.txt","w+")
            for word in bot.white_list:
                f.write(word+"\n")
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        
        
@bot.command()
async def get_censor_list(ctx):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        say = ""
        for word in sorted(bot.censor_list):
            say += word+"\n"
            if len(say) > 1900:
                await ctx.send(say)
                say = ""
        await ctx.send(say)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
 
 
@bot.command()
async def add_censor_list(ctx, word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        word = word.lower()
        if word not in bot.censor_list:
            bot.censor_list.append(word)
            f = open("censor_list.txt","a")
            f.write("\n"+word)
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()


@bot.command()
async def remove_censor_list(ctx, remove_word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        remove_word = remove_word.lower()
        if remove_word in bot.censor_list:
            f = open("censor_list.txt.bak","w+")
            for word in bot.censor_list:
                f.write(word+"\n")
            f.close()
            bot.censor_list.remove(remove_word)
            f = open("censor_list.txt","w+")
            for word in bot.censor_list:
                f.write(word+"\n")
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        

@bot.command()
async def get_consistency_list(ctx):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        say = ""
        for word in sorted(bot.consistency_list):
            say += word+"\n"
            if len(say) > 1900:
                await ctx.send(say)
                say = ""
        await ctx.send(say)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
 
 
@bot.command()
async def add_consistency_list(ctx, word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        word = word.lower()
        if word not in bot.censor_list:
            bot.consistency_list.append(word)
            f = open("consistency_list.txt","a")
            f.write("\n"+word)
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()


@bot.command()
async def remove_consistency_list(ctx, remove_word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        remove_word = remove_word.lower()
        if remove_word in bot.consistency_list:
            f = open("consistency_list.txt.bak","w+")
            for word in bot.consistency_list:
                f.write(word+"\n")
            f.close()
            bot.consistency_list.remove(remove_word)
            f = open("consistency_list.txt","w+")
            for word in bot.consistency_list:
                f.write(word+"\n")
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        
 
@bot.command()
async def get_mistakes_dict(ctx):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        say = ""
        for word in sorted(bot.mistakes_dict.keys()):
            say += word+"   :   "+bot.mistakes_dict[word]+"\n"
            if len(say) > 1900:
                await ctx.send(say)
                say = ""
        await ctx.send(say)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        
        
@bot.command()
async def add_mistakes_dict(ctx, wrong_word, correct_word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        wrong_word = wrong_word.lower()
        if wrong_word not in bot.mistakes_dict:
            bot.mistakes_dict[wrong_word] = correct_word
            f = open("mistakes_dict.txt","a")
            f.write("\n"+wrong_word+":"+correct_word)
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
        
        
@bot.command()
async def remove_mistakes_dict(ctx, wrong_word):
    if ctx.author.id not in bot.admins:
        await ctx.send("Haha denied! "+ctx.author.mention)
    else:
        wrong_word = wrong_word.lower()
        if wrong_word in bot.mistakes_dict:
            f = open("mistakes_dict.txt.bak","w+")
            for word in bot.mistakes_dict:
                f.write(word+":"+bot.mistakes_dict[word]+"\n")
            f.close()
            del bot.mistakes_dict[wrong_word]
            f = open("mistakes_dict.txt","w+")
            for word in bot.mistakes_dict:
                f.write(word+":"+bot.mistakes_dict[word]+"\n")
            f.close()
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()
 

@bot.command()
async def help(ctx):
    say = "**>adminhelp**\nWill show avaible admin commands.\n\n"
    say += "**>danishjoke**\nWill tell a danish pun but translated to english.\n\n"
    say += "**>help**\nWill show this message.\n\n"
    say += "**>latex** *string*\nWill render the string as mathmode-LaTeX and send it as a png.\n\n"
    say += "**>monospace** *string*\nWill render the string in monospace font and send it as a png."
    await ctx.send(say, delete_after=120)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()


@bot.command()
async def danishjoke(ctx):
    jokes = ["Why are asians yellow?\n||Because they **fucks** in curry!||",
             "Why dosen't icecubes have any arms or legs?\n||Because they are **watermade**!||",
             "What is the name of the worlds poorest king?\n||**King Course**!||",
             "Why has the Zoo in Odense never been sold?\n||Because it is too **animal**!||",
             "What do you call chinese rockers?\n||**Carrots**!||",
             "How do you get a fish to laugh?\n||You put it in **spring water**!||",
             "What is a pig called on Mars?\n||**Guinea pig**!||",
             "Why is it only fathers who can drink from Kattegat?\n||Because it is **fatherwater**!||"]
    joke_idx = np.random.randint(0, len(jokes))
    await ctx.send(jokes[joke_idx]+"  "+ctx.author.mention)
    if "Direct Message" not in str(ctx.channel):
        await ctx.message.delete()


@bot.command()
async def latex(ctx, *, arg):    
    try:
        SizeX = 0.1
        SizeY = 0.1
        plt.rc('font', size=24)
        fig = plt.figure(figsize=(SizeX, SizeY))
        plt.text(0,0,r"$"+arg+"$")
        plt.axis("off")
        plt.savefig("tmp.png", bbox_inches='tight')
        plt.close()
        await ctx.send(ctx.author.mention+" says:",file=File(os.path.dirname(os.path.abspath(__file__))+"/tmp.png"))
    except:
        await ctx.send("Math-LaTeX error in: "+ctx.message.content+" "+ctx.author.mention)
    await ctx.message.delete()
        
        
@bot.command()
async def monospace(ctx, *, arg):    
    try:
        SizeX = 0.1
        SizeY = 0.1
        plt.rc('font', size=12) 
        fig = plt.figure(figsize=(SizeX, SizeY))
        arg = arg.replace("$","\$")
        plt.text(0,0,arg,family="monospace")
        plt.axis("off")
        plt.savefig("tmp.png", bbox_inches='tight')
        plt.close()
        await ctx.send(ctx.author.mention+" says:",file=File(os.path.dirname(os.path.abspath(__file__))+"/tmp.png"))
    except:
        await ctx.send("Error in: "+ctx.message.content+" "+ctx.author.mention)
    await ctx.message.delete()
    

@bot.event
async def on_message(msg):
    if msg.author.id == bot.user.id:
        return
    
    
    """Admins do commands before CENSORING"""
    if msg.author.id in bot.admins:
        if len(msg.content) > 0:
            if msg.content[0] == ">":
                await bot.process_commands(msg)
                return
       
       
    """DELETE MUSIC BOT MSG"""
    if len(msg.content) > 1:
        if msg.content[0:2] == ";;":
            await msg.delete(delay=20)
            return
    if msg.author.id == 184405311681986560: #music bot
        await msg.delete(delay=20)
        return
    
    
    """CENSORING"""
    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    censored_msg = msg.content.lower()
    censored = False
    for item in bot.censor_list:
        if item in censored_msg:
            censored_msg = censored_msg.replace(item,"□"*len(item))
            censored = True
    if censored == True:
        censored_msg = list(censored_msg)
        for i, letter in enumerate(censored_msg):
            if letter != "□":
                censored_msg[i] = msg.content[i]
        censored_msg = "".join(censored_msg)
        censored_word = censored_msg.split(" ")
        original_word = msg.content.split(" ")
        for i in range(len(censored_word)):
            if "□" in censored_word[i]:
                for item in bot.white_list:
                    if item in original_word[i].lower():
                        censored_word[i] = original_word[i]
                        break
        for i in range(len(censored_word)):
            if "□" in censored_word[i]:
                new_word = ""
                for letter in censored_word[i]:
                    if letter in ascii_letters:
                        new_word += "□"
                    else:
                        new_word += letter
                censored_word[i] = new_word
        censored_msg = " ".join(censored_word)
        if "□" in censored_msg and censored_msg[0] != ">" and censored_msg[0:2] != ";;":
            await msg.channel.send(msg.author.mention+" says(censored version):\n"+censored_msg)
            if "Direct Message" not in str(msg.channel):
                await msg.delete()
            msg.content = censored_msg
        elif "□" in censored_msg:
            msg.content = censored_msg
    
    
    """Doing commands"""
    if msg.author.id not in bot.admins:
        if len(msg.content) > 0:
            if msg.content[0] == ">":
                await bot.process_commands(msg)
                return
         
         
    """IM RESPONSE"""
    iam_list = ["im ", "i'm ", "i am ", "Im ", "I'm ", "I am ", "I AM ", "I'M "]
    if len(msg.content.split()) < 7:
        for item in iam_list:
            if item in msg.content[0:5]:
                await msg.channel.send("Hello " + msg.content[0:5].replace(item,"") + msg.content[5:] + ", I'm Peter Bot!")
                return
    
        
    """SPELL CHECK"""
    found_list = []
    for word in msg.content.lower().replace(",","").replace(".","").replace("!","").replace("?","").split():
        if word in bot.mistakes_dict:
            if word not in found_list:
                await msg.channel.send("Ackchyually *"+word+"* is spelled *"+bot.mistakes_dict[word]+"*. "+msg.author.mention)
                found_list.append(word)
                
                
    """SOME CUSTOM RESPONSES"""
    if in_message("69", msg.content):
        await msg.channel.send("Hehe 69")
    if in_message("420", msg.content):
        await msg.channel.send("420 blaze it")
    if in_message("9/11", msg.content):
        await msg.channel.send("Bush did 9/11")
    if in_message("1337", msg.content):
        await msg.channel.send("1337 is leet")
    if message_is("hello there", msg.content.lower()):
        await msg.channel.send("General Kenobi")
    if message_is("hotel", msg.content.lower()):
        await msg.channel.send("Trivago")


@bot.event
async def on_message_edit(old_msg, msg):
    if msg.author.id == bot.user.id:
        return
    if msg.author.id == 184405311681986560: #music bot
        return

    """CENSORING"""
    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    censored_msg = msg.content.lower()
    censored = False
    for item in bot.censor_list:
        if item in censored_msg:
            censored_msg = censored_msg.replace(item,"□"*len(item))
            censored = True
    if censored == True:
        censored_msg = list(censored_msg)
        for i, letter in enumerate(censored_msg):
            if letter != "□":
                censored_msg[i] = msg.content[i]
        censored_msg = "".join(censored_msg)
        censored_word = censored_msg.split(" ")
        original_word = msg.content.split(" ")
        for i in range(len(censored_word)):
            if "□" in censored_word[i]:
                for item in bot.white_list:
                    if item in original_word[i]:
                        censored_word[i] = original_word[i]
                        break
        for i in range(len(censored_word)):
            if "□" in censored_word[i]:
                new_word = ""
                for letter in censored_word[i]:
                    if letter in ascii_letters:
                        new_word += "□"
                    else:
                        new_word += letter
                censored_word[i] = new_word
        censored_msg = " ".join(censored_word)
        if "□" in censored_msg:
            await msg.channel.send(msg.author.mention+" says(censored version):\n"+censored_msg)
            if "Direct Message" not in str(msg.channel):
                await msg.delete()
            msg.content = censored_msg
        

@bot.event
async def on_member_update(before, after):
    if before.id == bot.user.id:
        return
    
    """CENSORING"""
    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if after.nick != None:
        censored_msg = after.nick.lower()
        censored = False
        for item in bot.censor_list:
            if item in censored_msg:
                censored_msg = censored_msg.replace(item,"□"*len(item))
                censored = True
        if censored == True:
            censored_msg = list(censored_msg)
            for i, letter in enumerate(censored_msg):
                if letter != "□":
                    censored_msg[i] = after.nick[i]
            censored_msg = "".join(censored_msg)
            censored_word = censored_msg.split(" ")
            original_word = after.nick.split(" ")
            for i in range(len(censored_word)):
                if "□" in censored_word[i]:
                    for item in bot.white_list:
                        if item in original_word[i].lower():
                            censored_word[i] = original_word[i]
                            break
            for i in range(len(censored_word)):
                if "□" in censored_word[i]:
                    new_word = ""
                    for letter in censored_word[i]:
                        if letter in ascii_letters:
                            new_word += "□"
                        else:
                            new_word += letter
                    censored_word[i] = new_word
            censored_msg = " ".join(censored_word)
            censored_msg = " ".join(censored_word)
            if "□" in censored_msg:
                await after.edit(nick=censored_msg)

 
def in_message(word, msg):
    if word in msg.split():
        return True
    return False
    
    
def message_is(word, msg):
    if word == msg:
        return True
    else:
        endlist = [".","?","!"]
        for item in endlist:
            if word == msg+item:
                return True
    return False


with open('TOKEN') as f:
    TOKEN = f.readline()
bot.run(TOKEN)
