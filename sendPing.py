import discord, time
from func import *
time.sleep(10)
TOKEN = ("token")
client2 = discord.Client()

@client2.event
async def on_ready():
    print("2 on")
    while True:
        clientTwo = readFile("changes.txt")
        if clientTwo != []:
            print(clientTwo)
            arr = getArr("masterCourses.txt")
            requests = readRequestsArr()
            for x in requests:
                for y in clientTwo:
                    
                    if x[2] == y[:-1]:
                        channel = client2.get_channel(int(x[4]))
                        await channel.send("Spots in **" + x[2] + "** *(" + x[0] + "-" + x[1] + ")*" + ": " + crnToSub(x[2],arr)[2])
            writeFile("changes.txt", "")
        time.sleep(1)

client2.run(TOKEN)