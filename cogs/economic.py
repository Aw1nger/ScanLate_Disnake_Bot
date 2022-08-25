from http import client
from select import select
import disnake
from disnake.ext import commands
from pymongo import MongoClient
from disnake.ui import Select, View
import time
import datetime
import random
import config

cluster = MongoClient("mongodb+srv://aw1nger:YbrbnF2005@data.4htkyxj.mongodb.net/?retryWrites=true&w=majority")
eco = cluster.data.economic
status = cluster.data.status

class Dreamland():

    """Расчеты для мира грёз"""

    def __init__(self, start_sleep):
        self.start_sleep = start_sleep

    def hours(self):

        """Часы которые ты пробыл в Мире Грёз"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 8:
            hours = 8
            return hours
        else:
            return int(hours)

    def minutes(self):
        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 8:
            minutes = 0
            return int(minutes)
        else:
            minutes = sleep_time - (hours * 60)
            return int(minutes)
    
    def sparkles(self):

        """Расчет количества spark-ов"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 8:
            earn_sparked = 4600 + random.randint(0, 400)
            return int(earn_sparked)
        else:
            earn_sparked = 9.16 * int(sleep_time) + random.randint(0, 50)
            return int(earn_sparked)
    
    def red_sparkles(self):

        """Расчет количества red_spark-ов"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 8:
            earn_red_sparkles = -1.7 // (8 - 8.3)
            return int(earn_red_sparkles)
        else:
            earn_red_sparkles = -1.7 // (int(hours) - 8.3)
            return int(earn_red_sparkles)

    def bad_or_good_event(self):

        """Случилось ли что нибудь user был в МГ"""

        now = time.time()
        event = None
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        minutes = sleep_time - (hours * 60)
        if minutes <= 60:
            bad_interest = 187.6 // (minutes + 2.68)
            if random.randint(0, 100) <= bad_interest:
                event = 'bad'
        else:
            if hours >= 8:
                hours = 8
            bad_interest = int(hours) + 2
            if random.randint(0, 100) <= bad_interest:
                event = 'bad'
            good_event = int(hours) + 2
            if random.randint(0, 100) <= good_event:
                event = 'good'
        return event

    def bonus_sparkles(self):

        """Бонусные Sparkles при хорошем ивенте"""

        bonus_sparkles = random.randint(750, 3000)
        return bonus_sparkles

    def bonus_red_sparkles(self):

        """Бонусные Red_Sparkles при хорошем ивенте"""

        bonus_red_sparkles = random.randint(3, 7)
        return bonus_red_sparkles

    def minus_sparkles(self):

        """Потеря Sparkles при отрицательном ивенте"""

        minus_sparkles = random.randint(700, 1500)
        return minus_sparkles

    def minus_red_sparkles(self):

        """Потеря Red_Sparkles при отрицательном ивенте"""

        minus_red_sparkles = random.randint(2, 5)
        return minus_red_sparkles

    

class Nightmare():

    """Расчет валюты для Кошмарной пустоши"""

    def __init__(self, start_sleep):
        self.start_sleep = start_sleep

    def hours(self):

        """Часы которые ты пробыл в Кошмарной Пустоши"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 12:
            hours = 12
            return int(hours)
        else:
            return int(hours)

    def minutes(self):

        """Минуты которые ты провел в Кошмарной Пустоши"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 12:
            minutes = 0
            return int(minutes)
        else:
            minutes = sleep_time - (hours * 60)
            return int(minutes)
    
    def sparkles(self):

        """Звёздочки которые ты собрал в КП"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 12:
            earn_sparked = 1100 + random.randint(0, 50)
            return int(earn_sparked)
        else:
            earn_sparked = 1.52 * int(sleep_time) + random.randint(-30, 30)
            return int(earn_sparked)
    
    def red_sparkles(self):

        """Красный звездочки которые ты собрал в КП"""

        now = time.time()
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        if hours >= 12:
            earn_red_sparkles = 1.09 * int(hours) + 1.91
            return int(earn_red_sparkles)
        else:
            earn_red_sparkles = 1.09 * int(hours) + 1.91
            return int(earn_red_sparkles)

    def bad_or_good_event(self):

        """Случилось ли что нибудь user был в КП"""

        now = time.time()
        event = None
        sleep_time = (now - self.start_sleep) // 60
        hours = sleep_time // 60
        minutes = sleep_time - (hours * 60)
        if minutes <= 60:
            bad_interest = 3115.35 // (minutes + 34.615)
            if random.randint(0, 100) <= bad_interest:
                event = 'bad'
        else:
            if hours >= 12:
                hours = 12
            bad_interest = 0.5 * int(hours) + 24
            if random.randint(0, 100) <= bad_interest:
                event = 'bad'
            good_event = int(hours) + 2
            if random.randint(0, 100) <= good_event:
                event = 'good'
        return event

class Dreamland_event():

    """Проверка случился ли какой-нибудь ивент и обновление БД"""

    def __init__(self, dreamland, event):
        self.dreamland = dreamland
        self.event = event
    
    def reply(self, inter):
        if self.event is None:

            status.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"sleep": False, "start_sleep": None}})

            balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["balance"]
            red_balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["red_balance"]
            plus_bal = self.dreamland.sparkles()
            plus_red_bal = self.dreamland.red_sparkles()
            print(f"{plus_bal} | {plus_red_bal}")

            eco.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"balance": balance + plus_bal, "red_balance": red_balance + plus_red_bal}})

            embed = disnake.Embed(
                    title = f"С возращением! Вы занимались сбором {self.dreamland.hours()} часов {self.dreamland.minutes()} минут.",
                    description=f"Вы вернулись из **Мира Грёз** и принесли с собой **{plus_bal}**<:sparkles_mix:1011173769416552489> и **{plus_red_bal}**<:sparkles_red:1011173774936248390>",
                    color=0xFF00FF
                )

            return embed

        elif self.event == 'good':

            status.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"sleep": False, "start_sleep": None}})

            balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["balance"]
            red_balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["red_balance"]
            plus_bal = self.dreamland.sparkles()
            plus_red_bal = self.dreamland.red_sparkles()
            bonus_bal = self.dreamland.bonus_sparkles()
            bonus_red_bal = self.dreamland.bonus_red_sparkles()

            eco.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"balance": balance + plus_bal + bonus_bal, "red_balance": red_balance + plus_red_bal + bonus_red_bal}})

            embed = disnake.Embed(
                    title = f"С возращением! Вы занимались сбором {self.dreamland.hours()} часов {self.dreamland.minutes()} минут.",
                    description=f"Возращаясь из **Мира Грёз** вы заметеили падающую звезду и получили бонусные {bonus_bal}<:sparkles_mix:1011173769416552489> и {bonus_red_bal}<:sparkles_red:1011173774936248390>\n По итогу вы принесли **{plus_bal + bonus_bal}**<:sparkles_mix:1011173769416552489> и **{plus_red_bal + plus_red_bal}**<:sparkles_red:1011173774936248390>",
                    color=0xFF00FF
                )

            return embed

        else:

            status.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"sleep": False, "start_sleep": None}})

            balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["balance"]
            red_balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["red_balance"]
            minus_bal = self.dreamland.minus_sparkles()
            minus_red_bal = self.dreamland.minus_red_sparkles()
            
            if minus_bal >= balance:
                minus_bal = balance

            if minus_red_bal >= red_balance:
                minus_red_bal = red_balance

            eco.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"balance": balance - minus_bal, "red_balance": red_balance - minus_red_bal}})

            embed = disnake.Embed(
                    title = f"С возращением! Вы занимались сбором {self.dreamland.hours()} часов {self.dreamland.minutes()} минут.",
                    description=f"Слишком увлекшись сбором, вы не змаетили как к вам сзади подкрался кошмарик и съел ваши звездочки, к сожалению вы потеряли {minus_bal}<:sparkles_mix:1011173769416552489> и {minus_red_bal}<:sparkles_red:1011173774936248390>",
                    color=0xFF00FF
                )

            return embed


class SleepSelect(View):
    @disnake.ui.select(
            placeholder="Выберите куда хотите отправиться:",
            min_values=1,
            max_values=1,
            options=[
                disnake.SelectOption(
                    label="Мир Грёз", description="Спокойное место, где можно ничего не опасясь собирать звездочки.", emoji="<:sparkles_mix:1011173769416552489>"
                ),
                disnake.SelectOption(
                    label="Кошмарная Пустошь", description="Территория опасностей. Но чем выше риск, тем лучше награда.", emoji="<:sparkles_red:1011173774936248390>"
                )]
        )

    async def select_callback(self, select, inter):
        select.disabled=True
        await inter.response.edit_message(view=self)
        if select.values[0] == "Мир Грёз":
            status.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"sleep": 'dreamland', "start_sleep": time.time()}})
            await inter.followup.send(embed = disnake.Embed(description = f"Вы отправились в **Мир Грёз**<:sparkles_pink:1011173771463381053>",color=0xff6b81))

        elif select.values[0] == "Кошмарная Пустошь":
            status.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"sleep": 'nightmare', "start_sleep": time.time()}})
            await inter.followup.send(embed = disnake.Embed(description=f"Вы отправились в **Кошмарную Пустошь**<:sparkles_white:1011173776735612959>", color=0xff0000))

class economic(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name = 'balance',
        description = 'Узнайте ваш баланс'
    )
    async def balance(self, inter: disnake.ApplicationCommandInteraction):
        guild_id = inter.author.guild.id
        member_id = inter.author.id
        print(str(guild_id) + '|' + str(member_id))
        balance = eco.find_one({"guild_id": guild_id, "member_id": member_id})['balance']
        red_balance = eco.find_one({"guild_id": guild_id, "member_id": member_id})['red_balance']
        bank_balance = eco.find_one({"guild_id": guild_id, "member_id": member_id})['bank_balance']
        bank_red_balance = eco.find_one({"guild_id": guild_id, "member_id": member_id})['bank_red_balance']
        embed = disnake.Embed(
            description = '**Ваш баланс составляет:**',
            color = 0xfefe22,
            timestamp = datetime.datetime.today()
        )
        embed.add_field(name = 'На руках:', value = '➥')
        embed.add_field(name = '<:sparkles_mix:1011173769416552489>', value = f'**{balance}**')
        embed.add_field(name = '<:sparkles_red:1011173774936248390>', value = f'**{red_balance}**')
        embed.add_field(name = 'В банке:', value = '➥')
        embed.add_field(name = '<:sparkles_mix:1011173769416552489>', value = f'**{bank_balance}**')
        embed.add_field(name = '<:sparkles_red:1011173774936248390>', value = f'**{bank_red_balance}**')
        embed.add_field(name = 'Всего:', value = '➥')
        embed.add_field(name = '<:sparkles_mix:1011173769416552489>', value = f'**{balance + bank_balance}**')
        embed.add_field(name = '<:sparkles_red:1011173774936248390>', value = f'**{red_balance + bank_red_balance}**')
        embed.set_author(name = f'Баланс пользователя {inter.author.display_name}', icon_url = 'https://ie.wampi.ru/2022/08/18/Sparkles9dd549efe912e41a.gif')
        embed.set_thumbnail(url = f'{inter.author.display_avatar.url}')
        embed.set_footer(text = f'{inter.author.guild.name}', icon_url = f'{inter.author.guild.icon.url}')
        await inter.response.send_message( embed = embed)

    '''@commands.slash_command(
        name = 'top_balance',
        dascription = 'Выводит топ пользователей по балансу'
    )
    async def top_bal(self):
        for i in range():
            hui'''

    @commands.slash_command(
        name='sleep',
        description='Отправьтесь собирать звездочки'
    )
    async def sleep(self, inter: disnake.ApplicationCommandInteraction):

        if 'dreamland' == status.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["sleep"]:
            start_sleep = status.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["start_sleep"]
            dreamland = Dreamland(start_sleep=start_sleep)
            event = Dreamland_event(dreamland=dreamland, event=dreamland.bad_or_good_event())
            await inter.send(embed = event.reply(inter=inter))

        elif 'nightmare' == status.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["sleep"]:

            start_sleep = status.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["start_sleep"]
            status.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"sleep": False, "start_sleep": None}})

            nightmare = Nightmare(start_sleep=start_sleep)
            balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["balance"]
            red_balance = eco.find_one({"guild_id": inter.author.guild.id, "member_id": inter.author.id})["red_balance"]
            plus_bal = nightmare.sparkles()
            plus_red_bal = nightmare.red_sparkles()
            print(f"{plus_bal} | {plus_red_bal}")

            eco.update_many({"guild_id": inter.author.guild.id, "member_id": inter.author.id},
            {"$set": {"balance": balance + plus_bal, "red_balance": red_balance + plus_red_bal}})

            await inter.send(embed = disnake.Embed(
                    title = f"С возращением! Вы занимались сбором {nightmare.hours()} часов {nightmare.minutes()} минут.",
                    description=f"Вы вернулись из **Кошмарной Пустоши** и принесли с собой **{plus_bal}**<:sparkles_mix:1011173769416552489>  и **{plus_red_bal}**<:sparkles_red:1011173774936248390>",
                    color=0x8B008B
                ))
        else:
            view = SleepSelect()
            await inter.response.send_message("Выберите куда хотите отправиться:", view=view, ephemeral=True)

def setup(client):
    client.add_cog(economic(client))