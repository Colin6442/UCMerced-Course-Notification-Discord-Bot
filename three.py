import discord, time
from BetterBot.func import *

TOKEN = ("Discord Token Here")
client2 = discord.Client()

@client2.event
async def on_ready():
    print("2 on")
    while True:
        clientTwo = readFile("changes.txt")
        if clientTwo != []:
            requests = readRequestsArr()
            for x in requests:
                for y in clientTwo:
                    if x[2] == y:
                        channel = client2.get_channel(int(x[4]))
                        await channel.send("Spots in **" + x[2] + "** *(" + x[0] + "-" + x[1] + ")*" + ": " + x[3])
            writeFile("changes.txt", "")
        time.sleep(1)

client2.run(TOKEN)