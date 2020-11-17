import discord
from BetterBot.func import *

TOKEN = ("Discord Token Here")
client = discord.Client()


@client.event
async def on_ready():
    print("1 on")
    await client.change_presence(status= discord.Status.online, activity= discord.Game("!info for info"))


@client.event
async def on_message(message):
    if message.author != client.user:
        arr = getArr("masterCourses.txt")
        if message.content == "!info":
            await message.channel.send("```!crn \"number\" \t\t\t\t\t Adds class to pings \n"
                                       "!check \"subject-number\" \t\t\t\t\t Checks if the class is available right now \n"
                                       "!classes   \t\t\t\t\t\t\t\t  Returns list of classes assigned to this channel \n"
                                       "!remove    \t\t\t\t\t\t\t\t  Coming Soon```")

        if message.content[0:6] == "!check":
            try:
                next = message.content.find("-")
                sub = message.content[7:next].upper()
                num = message.content[next + 1:]
                if len(num) == 1:
                    num = "00" + num
                if len(num) == 2:
                    num = "0" + num
                checking = getClassList(sub, num, arr)
                if len(checking) > 0:
                    for x in checking:
                        await message.channel.send("\t\t\tCRN: " + str(arr[2][x]) + " has " + str(arr[3][x]) + " spots left")
                else:
                    await message.channel.send("No classes available as of right now")
            except:
                await message.channel.send("Error Processing \'!check\', check that you entered the command correctly")


        """if message.content[0:4] == "!sub":
            try:
                next = message.content.find("-")
                sub = message.content[5:next].upper()
                num = message.content[next+1:]
                if len(num) == 1:
                    num = "00" + num
                if len(num) == 2:
                    num = "0" + num
                if checkClassExists(sub, num):
                    go = True
                    for x in allRequets(message.channel.id)[0]:
                       if x == (sub + " " + num):
                           go = False
                    if go:
                        requests.append(addRequest(message.channel.id, sub, num))
                        await  message.channel.send("Added **" + sub + "-" + num + "** to ***" + str(message.channel) + "***")
                    else:
                        await  message.channel.send("Already added to this channel")
                else:
                    await  message.channel.send("Could not find class / does not exist")
            except:
                await message.channel.send("Error Processing \'!sub\', check that you entered the command correctly")"""


        if message.content[0:4] == "!crn":
            try:
                crn = message.content[5:]
                temp = crnToSub(crn, arr)
                if temp == None:
                    await message.channel.send("Invalid CRN: " + crn)
                else:
                    sub = temp[0]
                    num = temp[1]
                    if checkClassExists(sub, num, arr):
                        go = True
                        for x in readRequestsArr():
                            if x[2] == (crn):
                                go = False
                        if go:
                            appendRequests(crn, arr, message.channel.id)
                            await message.channel.send("Added **" + sub + "-" + num + "("+ crn +")" + "** to ***" + str(message.channel) + "***")
                        else:
                            await message.channel.send("Already added to this channel")
                    else:
                        await message.channel.send("Could not find class / does not exist")
            except:
                await message.channel.send("Error Processing \'!crn\', check that you entered the command correctly")


        if message.content[0:7] == "!remove":
            crn = message.content[8:]
            temp = crnToSub(crn, arr)
            go = True
            if temp == None:
                await message.channel.send("Invalid CRN: " + crn)
            else:
                for x in readRequestsArr():
                    if x[2] == crn and x[4] == str(message.channel.id):
                        removeRequests(crn)
                        await message.channel.send("**" + crn + "** was removed from ***" + str(message.channel) + "***")
                        go = False
                        break
                if go:
                    await message.channel.send("Class not found in this channel")



        if message.content[0:8] == "!classes":
            await  message.channel.send("Classes currently in this channel: ")
            for x in readRequestsArr():
                if x[4] == str(message.channel.id):
                    await message.channel.send("**" + x[2] + "**")


        if message.content[0:10] == "!channelID":
            await message.channel.send(message.channel.id)

client.run(TOKEN)




