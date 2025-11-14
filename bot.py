import discord
from discord.ext import commands
import json
import os
import random
import string
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "users.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

@bot.event
async def on_ready():
    print(f"[BOT] Online como {bot.user}")

@bot.command()
async def register(ctx, webhook_url: str = None):
    if ctx.guild:
        await ctx.send("Envie no privado!")
        return

    if not webhook_url or "discord.com/api/webhooks" not in webhook_url:
        await ctx.send("Webhook inválido!\nEx: `!register https://discord.com/api/webhooks/...`")
        return

    key = generate_key()
    user_id = str(ctx.author.id)

    users[user_id] = {
        "key": key,
        "webhook": webhook_url,
        "username": str(ctx.author)
    }
    save_users()

    await ctx.send(f"**KEY GERADA!**\n\n`{key}`\n\nCole no script do Romel!")
    print(f"[BOT] Key gerada para {ctx.author}: {key}")

@bot.command()
async def minhakey(ctx):
    if ctx.guild:
        await ctx.send("Envie no privado!")
        return
    user_id = str(ctx.author.id)
    if user_id in users:
        await ctx.send(f"Sua key: `{users[user_id]['key']}`")
    else:
        await ctx.send("Você não tem key. Use `!register <webhook>`")

# Rodar
bot.run(os.getenv("DISCORD_TOKEN"))
