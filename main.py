import discord
import json
import os
import tensorflow as tf
from classificar import prediction

js = open('token.json')
useful = json.load(js)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot_channel_id = useful['canal']


@client.event
async def on_ready():
    print(f'{client.user} está online!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == bot_channel_id:
        if str(message.content).startswith("!predict") and message:
            if len(message.attachments) == 0:
                await message.channel.send("To vendo nada não!\nTem certeza q tem uma imagem ai? >:D")
                return
            elif len(message.attachments) > 1:
                await message.channel.send("Calma ai cara >:(, só consigo analisar uma imagem de cada vez")
                return
            elif str(message.attachments[0].url).split(".")[-1] not in useful["image_format"]:
                await message.channel.send("EI! EU só aceito jpg, jpeg ou png :V")
                return
            predicao = prediction(message.attachments[0].url)
            await message.channel.send(f'{predicao}')

        if message.content.lower().startswith('oi'):
            await message.channel.send(f'Oi {message.author}, tudo bem?')


client.run(useful['token'])
