import asyncio
import discord
import requests
import re


async def get_cash(message):
    last_value = 0

    while True:
        page_content = requests.get(url='https://www.escapefromtarkov.com/cash').text
        matching_content = re.compile("var x = (\\d+),", re.MULTILINE).findall(page_content)
        new_value = int(matching_content.pop())
        if last_value != new_value:
            diff = new_value - last_value
            percentage = new_value / 1500000000000
            if last_value != 0:
                try:
                    await message.channel.send(
                        "Current: {} Diff: {} Progress: {}".format(f"{new_value:,}", f"{diff:,}", f"{percentage:.2%}"))
                except Exception:
                    print("Something went wrong in channel {}", message.channel)

            last_value = new_value
        await asyncio.sleep(5)


class EftCashBot(discord.Client):
    running = False

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content == "startEftCash" and self.running is False:
            print("start in {}".format(message.channel))
            self.running = True
            asyncio.get_event_loop().create_task(get_cash(message))
            try:
                await message.channel.send("Waiting for cash updates")
            except Exception:
                print("Something went wrong in channel {}", message.channel)

        if message.content == "stopEftCash" and self.running:
            print("stop in {}".format(message.channel))
            self.running = False
            try:
                await message.channel.send("Stopped the cash updates")
            except Exception:
                print("Something went wrong in channel {}", message.channel)
            asyncio.get_event_loop().stop()


intents = discord.Intents.default()
client = EftCashBot(intents=intents)
client.run('TOKEN')
