from http import client
import disnake
from disnake.ext import commands
from typing import Literal
import config
from pymongo import MongoClient
import datetime
import os
import random

class funnies(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name='roll',
        description='Случайное число из 100 или нужного тебе диапазона'
    )
    async def roll(self, inter: disnake.ApplicationCommandInteraction, amount: int = None):
        amount = amount or 100
        await inter.response.send_message(f"Roll(0 — {amount}): `{random.randint(0, amount)}`")

    @commands.slash_command(
        name='kill_0dmin',
        description='Неважно какой ты нации, ориентации или пола. Важно что админ хуесосос!'
    )
    @commands.cooldown(rate=1, per= 60 * 60 * 12, type=commands.BucketType.guild)
    async def kill_admin(self, inter: disnake.ApplicationCommandInteraction, content: str = None):
        if content is not None:
            content = '>>> ' + content
        else:
            content = ''
        embed = disnake.Embed(
            title=f"{inter.author.name} убил админа!",
            description=f"{content}",
            color=0xff335c,
            timestamp=datetime.datetime.today()
        )
        embed.set_footer(text='За что-о-о-о 😭')
        embed.set_image(url = f"{random.choice(config.kill_admin)}")
        await inter.response.send_message(embed = embed)

    @kill_admin.error
    async def cog_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: Exception):

        if isinstance(error, commands.CommandOnCooldown):
            cd_time = error.retry_after
            hours = int(cd_time) // (60 * 60)
            minutes = (int(cd_time) - (int(hours) * 3600)) // 60

            if hours != 0:
                await inter.response.send_message(embed = disnake.Embed(
                    title = 'Кто-то уже убил админа',
                    description=f'Вы повторно можете убить админа через {int(hours)} часов {int(minutes)} минут',
                    color=0xff335c
                ))

            else:
                await inter.response.send_message(embed = disnake.Embed(
                    title = 'Кто-то уже убил админа',
                    description=f'Вы повторно можете убить админа через {int(minutes)} минут',
                    color=0xff335c
                ))

    @commands.slash_command(
        name='poshol_nahuy',
        description='Послать нахуй кого угодно!'
    )
    @commands.cooldown(rate=1, per=60*5, type=commands.BucketType.user)
    async def poshol_nahuy(inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None, content: str = None):
        if content is not None:
            content = '>>> ' + content
        else:
            content = ''

        if member is None:
            embed = disnake.Embed(
                title = f'__**{inter.author.name}**__ послал всех нахуй!',
                description = f"{content}",
                color = 0xFF0066
                )
        else:
            embed = disnake.Embed(
                title = f"__**{inter.author.name}**__ послал нахуй __**{member.name}**__!",
                description = f"{content}",
                color = 0xFF0066
            )
        embed.set_image(url = f"{random.choice(config.poshol_nahuy)}")
        await inter.response.send_message(embed = embed)

    @poshol_nahuy.error
    async def cog_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: Exception):

        if isinstance(error, commands.CommandOnCooldown):
            cd_time = error.retry_after
            hours = int(cd_time) // (60 * 60)
            minutes = (int(cd_time) - (int(hours) * 3600)) // 60

            await inter.response.send_message(embed = disnake.Embed(
                title = 'Ты уже посылал нахуй за последние 5 минут!',
                description=f'Попробуй через {int(minutes)} минут!',
                color=0xFF0066
            ))


def setup(client):
    client.add_cog(funnies(client))