import disnake
from disnake.ext import commands
import config
from pymongo import MongoClient
import os

client = commands.Bot(command_prefix=config.Settings['prefix'], intents = disnake.Intents.all(), case_insensitive = True, strip_after_prefix = True)

cluster = MongoClient("mongodb+srv://aw1nger:YbrbnF2005@data.4htkyxj.mongodb.net/?retryWrites=true&w=majority")
collection_sc = cluster.data.scanlate
collection_type = cluster.data.channel_type
eco = cluster.data.economic
status = cluster.data.status

@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence( status = disnake.Status.online, activity = disnake.Game( 'Работаю, но не так как надо!' ))

    for guild in client.guilds:
        for member in guild.members:
            print(str(member.guild.id) + '|' + str(member.id))
            post_eco = {
                "guild_id": member.guild.id,
                "member_id": member.id,
                "balance": 1000,
                "red_balance": 0,
                "bank_balance": 0,
                "bank_red_balance": 0
            }

            post_status = {
                "guild_id": member.guild.id,
                "member_id": member.id,
                "status": 'wait',
                "sleep": False,
                "start_sleep": None  
            }

            if eco.count_documents({"guild_id": member.guild.id, "member_id": member.id}) == 0:
                eco.insert_one(post_eco)

            if status.count_documents({"guild_id": member.guild.id, "member_id": member.id}) == 0:
                status.insert_one(post_status)

@client.event
async def on_member_join(member):
	post_eco = {
        "guild_id": member.guild.id,
		"member_id": member.id,
		"balance": 1000,
		"red_balance": 0,
        "bank_balance": 0,
        "bank_red_balance": 0
    }

	if eco.count_documents({"guild_id": member.guild.id, "member_id": member.id}) == 0:
		eco.insert_one(post_eco)

@client.event
async def on_member_join(member):
    post_status = {
            "guild_id": member.guild.id,
            "member_id": member.id,
            "status": 'wait',
            "sleep": False,
            "start_sleep": None  
        }

    if status.count_documents({"guild_id": member.guild.id, "member_id": member.id}) == 0:
            status.insert_one(post_status)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(config.Settings['token'])