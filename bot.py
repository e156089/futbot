import discord, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")
# Permiss
intents = discord.Intents.default()
intents.message_content = True # Leer comandos del chat

bot = commands.Bot(command_prefix='!', intents=intents)

# Esta función se ejecuta apenas el bot logra conectarse a Discord.
@bot.event
async def on_ready():
    print(f'Conectado')

@bot.command()
async def habla(ctx):
    await ctx.send('Puto el que lee')

print(TOKEN)
bot.run(TOKEN)