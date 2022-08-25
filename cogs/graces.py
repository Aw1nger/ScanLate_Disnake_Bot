from http import client
import disnake
from disnake.ext import commands
import random
import config


class graces(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name='kiss',
        description='Поцеловать пользователя'
    )
    async def kiss(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member , *, content = None):
        content = content or ''
        embed = disnake.Embed(
            title = f"__**{inter.author.name}**__ поцеловал __**{member.name}**__",
            description = f"{content}",
            color = 0xff7aaf) 
        embed.set_image( url = f"{random.choice(config.kiss)}")
        await inter.response.send_message(embed = embed)

    @commands.slash_command(
        name = 'hug',
        description = 'Обнять пользователя'
    )
    async def hug(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, *, content = None):
        content = content or ''
        embed = disnake.Embed(
            title = f"__**{inter.author.name}**__ обнял __**{member.name}**__",
            description = f"{content}",
            color = 0xff7aaf)
        embed.set_image( url = f"{random.choice(config.hug)}")
        await inter.response.send_message(embed = embed)

    @commands.slash_command(
        name = 'good_morning',
        description = 'Пожелать доброго утра!'
    )
    async def good_morning(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None, *, content = None):
        content = content or ''

        if member is None:
            embed = disnake.Embed(
                title = f'__**{inter.author.name}**__ пожелал всем доброго утра!',
                description = f"{content}",
                color = 0xfefe22
                )
        else:
            embed = disnake.Embed(
            title = f"__**{inter.author.name}**__ пожелал доброго утра __**{member.name}**__",
            description = f"{content}",
            color = 0xfefe22)
        embed.set_image( url = f"{random.choice(config.good_morning)}")
        await inter.response.send_message(embed = embed)

    @commands.slash_command(
        name = 'good_night',
        description = 'Пожелать спокойной ночи!'
    )
    async def good_night(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None, *, content = None):
        content = content or ''

        if member is None:
            embed = disnake.Embed(
                title = f'__**{inter.author.name}**__ пожелал всем спокойной ночи!',
                description = f"{content}",
                color = 0x6666ff
                )
        else:
            embed = disnake.Embed(
                title = f"__**{inter.author.name}**__ пожелал спокойной ночи __**{member.name}**__!",
                description = f"{content}",
                color = 0x6666ff
            )
        embed.set_image(url = f"{random.choice(config.good_night)}")
        await inter.response.send_message(embed = embed)
   

def setup(client):
	client.add_cog(graces(client))
