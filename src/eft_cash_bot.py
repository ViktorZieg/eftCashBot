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


def get_task_id(message):
    return message.guild.id + message.channel.id


class EftCashBot(discord.Client):
    tasks = {}

    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content == "startEftCash":
            task_id = get_task_id(message)
            if task_id in self.tasks:
                await message.channel.send("You already have a bot in this channel")
                print("{} tried to duplicate".format(task_id))
            else:
                print("Start id {} Server: {} Channel: {}".format(task_id, message.guild.name, message.channel.name))
                new_task = self.loop.create_task(get_cash(message))
                self.tasks[task_id] = new_task
                await message.channel.send("Waiting for cash updates")

        if message.content == "stopEftCash":
            task_id = get_task_id(message)
            if task_id in self.tasks:
                task = self.tasks[task_id]
                print("Stop id {} Server: {} Channel: {}".format(task_id, message.guild.name, message.channel.name))
                task.cancel()
                del self.tasks[task_id]
                await message.channel.send("Stopped the cash updates")
            else:
                await message.channel.send("There is no bot started")


intents = discord.Intents.all()
client = EftCashBot(intents=intents, loop=asyncio.new_event_loop())
client.run('TOKEN')
