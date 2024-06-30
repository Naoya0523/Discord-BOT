
import discord
import asyncio
import random
from figure3d import get_3dfigure
from figure import get_figure
from character import DATA
from character_comment import COMMENT
from average_score import get_MMR
from custom3 import get_player_stats
from custom3 import get_best_matchup
import pandas as pd
from summoner_data_to_excel import get_player_stastus_and_to_excel

#DiscordBotのトークン
token = ''
voice_list = ["kkc_killjoy.mp3", "kkc_gomen.mp3", "kkc_kirai.mp3", "kkc_sitaiuti.mp3"]
member = []
roll_list = ['TOP','JG', 'MID', 'ADC', 'SUP']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global voice_list, member, roll_list
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('```diff\nHello!\n```')

    if message.content.startswith('$join'):
        if message.author.voice and message.author.voice.channel:
            channel = message.author.voice.channel
            vc = await channel.connect()
        else:
            await message.channel.send('please join voice channel!')

    if message.content == '$kkc':
        voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
        if not voice_client:
            await message.channel.send('The BOT is not in a voice channel.')
            return

        index = random.randint(0, len(voice_list)-1)
        path = 'anotherfile/audio/' + voice_list[index]
        source = discord.FFmpegPCMAudio(path)
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(0.1)

    #LoL methodo
    if message.content.startswith('!'):
        #print(message.content.replace('!',''))
        name = str(message.content.replace('!',''))
        if get_figure(DATA, name):
            await message.channel.send(name + "'s status")

            with open('fig.png', 'rb') as f:
                image = discord.File(f)
            await message.channel.send(file=image)
            await message.channel.send(COMMENT[name])

        else:
            try:
                await message.channel.send(COMMENT[name])
            except Exception as e:
                name = name.split(',')
                if name[0] not in ['help', 'custom', 'shuffle', 'clear', 'shuffle-mmr']:
                    print(e)
                    await message.channel.send('character names wrong')

    #custom member function
    if message.content.startswith('!custom'):
        input_line = message.content.replace('!custom,','')
        try:
            summoner_name, positions = get_player_stats(input_line)
        except Exception as e:
            print(e)
            await message.channel.send(f'{message.author}, 入力を確かめて下さい')
            return

        try:
            test = pd.read_excel(f'excel files/{summoner_name}.xlsx')
        except Exception:
            await message.channel.send('データを取得します。最大で3分かかる場合があります。')
            if get_player_stastus_and_to_excel(summoner_name):
                await message.channel.send('データを取得しました。')
            else:
                await message.channel.send('データの取得に失敗しました。サモナーネームを確認してください。')
                return

        MMR = get_MMR(summoner_name)
        member.append({'name':summoner_name, 'position':positions, 'MMR':MMR})
        member_count = len(member)
        await message.channel.send('メンバーに追加しました。{}/10'.format(member_count))
        if len(member) == 10:
            await message.channel.send('メンバーが10人になりました')

    if message.content == '!shuffle':
        if len(member) == 10:
            for position in member:
                print(position)

            await message.channel.send('チーム分けを計算中…')

            custom_member_list = get_best_matchup(member)
            if len(custom_member_list) == 0:
                await message.channel.send('候補が見つかりませんでした。希望レーンを調整してください。')
            else:
                for member in custom_member_list:
                    await message.channel.send(member)
        else:
            await message.channel.send('メンバーが10人ではありません')

    if message.content.startswith('!clear'):
        member = []
        await message.channel.send('メンバーをリセットしました')

    if message.content == '!help':
        comment = []
        for key, value in COMMENT.items():
            comment.append(key)
        await message.channel.send(comment)

    if message.content == '$leave':
        for vc in client.voice_clients:
            await vc.disconnect()

client.run(token)