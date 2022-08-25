from http import client
import disnake
from disnake.ext import commands
import config
from pymongo import MongoClient
import time
import os
import random


class slash_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command( name = 'clear', description = 'Удаляет выбранное колличество сообщений')
    @commands.has_permissions( administrator = True )
    async def clear(inter: disnake.ApplicationCommandInteraction, amount: int = 1):
        await inter.channel.purge( limit = amount )
        await inter.response.send_message(embed = disnake.Embed(title = 'Очистка сообщений', description=f'Очищенно 0 из {amount} сообщений', color = 0xff0000))
        time.sleep( amount * 0.01)
        await inter.edit_original_message(embed = disnake.Embed(title = 'Очистка сообщений', description=f'Очищенно {amount} из {amount} сообщений', color = 0x19ff19))

def setup(client):
    client.add_cog(slash_commands(client))