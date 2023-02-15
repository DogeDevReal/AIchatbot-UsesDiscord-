import openai
import discord
import os

openai.api_key = "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"

client = discord.Client(intents=discord.Intents.all())

messages = []

character = "Pea"
channel = None

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith("!setchannel"):
        words = message.content.split(" ")
        global channel
        if len(words) == 2:
            channel = message.channel_mentions[0]
            await message.channel.send(f"Channel has been set to {channel.mention}.")
        else:
            await message.channel.send("No channel has been specified, use !setchannel <channel mention> to set a channel.")

    elif message.content.startswith("!set character"):
        words = message.content.split(" ")
        global character
        if len(words) >= 3:
            character = " ".join(words[2:])
            await message.channel.send(f"Character has been set to {character}.")
        else:
            await message.channel.send("No character has been specified, use !set character <character name> to set a character.")


    elif not message.content.startswith("!") and message.channel == channel:
        messages.append(message.content)
        if character:
            prompt = f"Act like {character} {messages[-1]}"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text

            if response:
                await channel.send(response)
            else:
                print("No response could be generated.")
        else:
            await message.channel.send("No character has been set, use !set character <character name> to set a character.")
    elif message.content.startswith("!") and not channel:
        await message.channel.send("No channel has been set, use !setchannel <channel mention> to set a channel.")

client.run("MTA3NDAyMTYzODg3NTY0NDAyNA.GepMrO.ge1_T2KvoPRyUVuBau5x61wvHxtopWN7H47iyQ")
