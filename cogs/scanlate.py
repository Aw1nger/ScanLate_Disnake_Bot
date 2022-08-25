from http import client
import disnake
from disnake.ext import commands
from typing import Literal
from pymongo import MongoClient
import re
import config

cluster = MongoClient("mongodb+srv://aw1nger:YbrbnF2005@data.4htkyxj.mongodb.net/?retryWrites=true&w=majority")
collection_sc = cluster.data.scanlate
collection_type = cluster.data.channel_type

class ScanLate(commands.Cog):
    
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        #await self.client.process_commands( message )
        if message.author.bot: 
            return
        group_id = message.channel.category_id #получаем id группы каналов
        channel_name = message.channel.name #получаем название канала
        channel_id = message.channel.id #получаем id канала
        content = message.content.lower()
        chapter_regex = re.compile(r'глава (\d*(.\d*)?)')
        stage_regex = re.compile(r'(перевод|редакт|клин|проверка клина|тайп|проверка тайпа|склейка|проверка склейки) готов')
        chapter = chapter_regex.search(content)
        stage = stage_regex.search(content)
        chapter_number = chapter.group(1)
        chapter_number = chapter_number.strip()
        chapter = chapter.group()
        chapter = chapter.strip()
        stage = stage.group()

        post  = {
                'channel_id': channel_id,
                'title': channel_name,
                'chapter': chapter,
                'translates': 'unready',
                'corrected': 'unready',
                'clean': 'unready',
                'clean_beta': 'unready',
                'type': 'unready',
                'type_beta': 'unready',
                'gluing': 'unready',
                'gluing_beta': 'unready',
            }

        if collection_sc.count_documents({'channel_id': channel_id, 'chapter': chapter}) == 0:
            collection_sc.insert_one(post)

        if stage in config.Scanlate['translate']:
            if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['translates'] == 'ready':
                embed = disnake.Embed( title = 'Воу! Ты что сделал два перевода на одну главу<:nani:997935945686978650>',
                    description = 'Извини, но перевод на эту главу уже готов, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                    color = 0x5cfaf2)
                await message.channel.send(embed = embed)
            else:
                collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                    {"$set": {'translates': 'ready'}})
                emb = disnake.Embed( title = f'Перевод на ' + chapter_number + ' главу готов!', description = 'Был готов перевод - редактор, приступай к работе.\n'
                                            'Пожалуйста, сделай все за 1 день<:Kanna_Heart:997935947243065485>', colour = 0x19ff19)
                await message.channel.send('<@&991247836060590080>', embed = emb)

    #если в stage редакт готов
        if stage in config.Scanlate['redakt']:
            if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['corrected'] == 'ready':
                embed = disnake.Embed( title = 'Воу! Ты что сделал два редакта на одну главу<:nani:997935945686978650>',
                    description = 'Извини, но редакт на эту главу уже готов, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                    color = 0x5cfaf2)
                await message.channel.send(embed = embed)
            else:
                collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                    {'$set': {'corrected': 'ready'}})
                if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['clean_beta'] == 'ready':
                    emb = disnake.Embed( title = 'Клин  и редакт на ' + chapter_number + ' главу готовы!', description = 'Клин и редакт готовы - тайпер, приступай к работе.\n'
                                                'Пожалуйста сделай все за 2 дня<:Kanna_Heart:997935947243065485>', colour = 0x19ff19)
                    await message.channel.send( '<@&991253066546417765>', embed = emb )
                elif collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['clean'] != 'ready':
                    emb = disnake.Embed( title = 'Редакт на ' + chapter_number +'готов!', description = 'Редакт готов, но тайперу чего-то не хватает<:nani:997935945686978650>\n'
                                                'Клинер, мы очень тебя ждем<:PepeHappy:992766246875578508>', colour = 0xff0000)
                    await message.channel.send('<@&991252762975277086>', embed = emb)
                elif collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['clean'] == 'ready':
                    emb = disnake.Embed( title = 'Редакт на ' + chapter_number +'готов!', description = 'Редакт готов, но тайперу чего-то не хватает<:nani:997935945686978650>\n'
                                                'Бета, проверь клин скорее, мы очень тебя ждем<:PepeHappy:992766246875578508>', colour = 0xff0000)
                    await message.channel.send('<@&1003615090790117427>', embed = emb)

    #если в stage клин готов
        if stage in config.Scanlate['clean']:
            if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['clean'] == 'ready':
                embed = disnake.Embed( title = 'Воу! Ты что сделал два клина на одну главу<:nani:997935945686978650>',
                    description = 'Извини, но клин на эту главу уже готов, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                    color = 0x5cfaf2)
                await message.channel.send(embed = embed)
            else:
                collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                {'$set': {'clean': 'ready'}})
                embed = disnake.Embed( title=f'Клин на ' + chapter_number + ' главу готов!',
                                    description='Клин для проверки готов - бета, приступай к работе.\n'
                                                'Пожалуйста, сделай все за 1 день<:Kanna_Heart:997935947243065485>',
                                    colour=0x19ff19)
                await message.channel.send( '<@&1003615090790117427>', embed = embed )

    # если в stage проверка клина готова
        if stage in config.Scanlate['clean_beta']:
            if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['clean_beta'] == 'ready':
                embed = disnake.Embed( title = 'Воу! Ты что сделал проверку клина два раза на одну главу<:nani:997935945686978650>',
                    description = 'Извини, но клин на эту главу уже проверили, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                    color = 0x5cfaf2)
                await message.channel.send(embed = embed)
            else:
                collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                    {"$set": {'clean_beta': 'ready'}})
                if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['corrected'] == 'ready':
                    embed = disnake.Embed( title = 'Клин  и редакт на ' + chapter_number + ' главу готовы!', description = 'Клин и редакт готовы - тайпер, приступай к работе.\n'
                                                'Пожалуйста сделайвсе за 2 дня<:Kanna_Heart:997935947243065485>', colour = 0x19ff19)
                    await message.channel.send( '<@&991253066546417765>', embed = embed )
                elif collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['corrected'] != 'ready':
                    embed = disnake.Embed( title = 'Клин на ' + chapter_number + ' готов!', description = 'Клин готов, но тайперу чего-то не хватает<:nani:997935945686978650>\n'
                                                'Редактор, мы очень тебя ждем<:PepeHappy:992766246875578508>', colour = 0xff0000)
                    await message.channel.send( '<@&991247836060590080>', embed = embed )
                elif collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['translates'] != 'ready':
                    embed = disnake.Embed( title = 'Переводчик, как дела?!', description = 'Уже готов клин на ' + chapter_number + ', а перевода все еще нет!\n'
                                                'Дорогой переводчик, постарайся перевести как можно  скорее<:PepeHappy:992766246875578508>', colour = 0xff0000) 
                    await message.channel.send( '<@&991247844814110720>', embed = embed )

    #если в stage тайп готов
        if stage in config.Scanlate['type']:
            if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['type'] == 'ready':
                embed = disnake.Embed( title = 'Воу! Ты что сделал тайп два раза на одну главу<:nani:997935945686978650>',
                    description = 'Извини, но тайп на эту главу уже готов, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                    color = 0x5cfaf2)
                await message.channel.send(embed = embed)
            else:
                collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                    {"$set": {'type': 'ready'}})
                embed = disnake.Embed( title=f'Тайп на ' + chapter_number + ' главу готов!',
                                    description='Тайп для проверки готов - бета, приступай к работе.\n'
                                                'Пожалуйста, сделай все за 1 день<:Kanna_Heart:997935947243065485>',
                                    colour=0x19ff19 )
                await message.channel.send( '<@&1003615090790117427>', embed = embed )

    #если в stage проверка тайпа готова
        if stage in config.Scanlate['type_beta']:
                try:
                    if collection_type.find_one({'channel_id': channel_id})['channel_type'] == 'manga':
                        emb = disnake.Embed(title='Глава ' + chapter_number + ' готова!',
                                            description='Залейте на сайт<a:jump_cat:1004666180755275806>',
                                            colour=0x19ff19)
                        await message.channel.send('<@&1003357628061204520>', embed=emb)
                        collection_sc.delete_one({'channel_id': channel_id, 'chapter': chapter})

                    elif collection_type.find_one({'channel_id': channel_id})['channel_type'] == 'manhwa':

                        if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['type_beta'] == 'ready':
                            embed = disnake.Embed( title = 'Воу! Ты что проверил тайп два раза<:nani:997935945686978650>',
                                description = 'Извини, но тайп на эту главу уже проверили, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                                color = 0x5cfaf2)
                            await message.channel.send(embed = embed)

                        else:
                            collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                                {"$set": {'type_beta': 'ready'}})
                            emb = disnake.Embed( title = 'Проверка тайпа готова!', description = 'Тайп проверен - склейщик, приступай к работе\n'
                                'Пожалуйста, сделай все за 1 день<:Kanna_Heart:997935947243065485>', colour = 0x19ff19)
                            await message.channel.send('<@&996845194735534180>', embed = emb)
                except:
                    emb = disnake.Embed( title = 'Установите тип канала', description = 'Установить тип канала можно командой `!type`\n'
                                                'В настоящий момент доступен тип `манга` или `манхва`', colour = disnake.Colour.red())
                    await message.channel.send( embed = emb )

        if stage in config.Scanlate['gluing']:
            if collection_sc.find_one({'channel_id': channel_id, 'chapter': chapter})['gluing'] == 'ready':
                embed = disnake.Embed( title = 'Воу! Ты что сделал склейку два раза на одну главу<:nani:997935945686978650>',
                    description = 'Извини, но склейка на эту главу уже готова, я не буду никого пинговать<:sparkles_red:1006501538325344256>',
                    color = 0x5cfaf2)
                await message.channel.send(embed = embed)
            else:
                collection_sc.update_one({'channel_id': channel_id, 'chapter': chapter},
                                {"$set": {'gluing': 'ready'}})
                emb = disnake.Embed( title = 'Склейка на ' + chapter_number + ' главу готов!', description = 'Склейка готова - бета, приступай к работе\n'
                                                'Пожалуйста, сделай все за 1 день<:Kanna_Heart:997935947243065485>', colour = disnake.Colour.green())
                await message.channel.send('<@&1003615090790117427>', embed = emb)

        if stage in config.Scanlate['gluing_beta']:
            emb = disnake.Embed(title='Глава ' + chapter_number + ' готова!',
                                description='Залейте на сайт<a:jump_cat:1004666180755275806>',
                                colour=0x19ff19)
            await message.channel.send('<@&1003357628061204520>', embed=emb)
            collection_sc.delete_one({'channel_id': channel_id, 'chapter': chapter})

    @commands.slash_command(
        name='channel_type',
        description='Установить тип канала'
    )
    @commands.has_permissions( administrator = True )
    async def type(self, inter: disnake.ApplicationCommandInteraction , channel_type: Literal['манга', 'манхва']):
        channel_id = inter.channel.id
        channel_type = channel_type.lower()

        if channel_type == 'манга':
            if collection_type.count_documents({'channel_id': channel_id}) == 0:
                post = {
                    'channel_id': channel_id,
                    'channel_type': 'manga'
                }
                collection_type.insert_one(post)
            else:
                collection_type.update_one({'channel_id': channel_id},
                    {"$set": {'channel_type':'manga'}})
            emb = disnake.Embed(title = 'Был установлен тип канала', description = 'Для данного канал установлен тип **манга**.', colour = 0x5cfaf2)
            emb.set_footer(text = f'{inter.author.guild.name}', icon_url = f'{inter.author.guild.icon.url}')
            await inter.response.send_message( embed = emb)

        if channel_type == 'манхва':
            if collection_type.count_documents({'channel_id': channel_id}) == 0:
                post = {
                    'channel_id': channel_id,
                    'channel_type': 'manhwa'
                }
                collection_type.insert_one(post)
            else:
                collection_type.update_one({'channel_id': channel_id},
                    {"$set": {'channel_type':'manhwa'}})
            emb = disnake.Embed(title = 'Был установлен тип канала', description = 'Для данного канал установлен тип **манхва**.', colour = 0x5cfaf2)
            emb.set_footer(text = f'{inter.author.guild.name}', icon_url = f'{inter.author.guild.icon.url}')
            await inter.response.send_message( embed = emb )

def setup(client):
	client.add_cog(ScanLate(client))