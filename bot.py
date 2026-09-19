import discord, os, datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv
from reporte import obtener_partidos, obtener_tabla

load_dotenv()
TOKEN_BOT = os.environ.get("TOKEN_BOT")

# Permisos
intents = discord.Intents.default()
intents.message_content = True # Leer comandos del chat

bot = commands.Bot(command_prefix='!', intents=intents)

# Esta función se ejecuta apenas el bot logra conectarse a Discord.
@bot.event
async def on_ready():
    print(f'Conectado')
    # buscar_info()
    # a = obtener_reporte()
    # if not reporte.is_running(): # Empezar loop
    #     reporte.start()


# hora = datetime.time(hour=0, minute=0)
# @tasks.loop(time=hora)
# async def reporte():
#     hoy = datetime.datetime.now()
#     # 0 = Lunes | 1 = Martes | 2 = Miércoles | 3 = Jueves 
#     # 4 = Viernes | 5 = Sábado | 6 = Domingo
#     if hoy.weekday() == 1:
#         ID_DEL_CANAL = 1398376928716652697
#         canal = bot.get_channel(ID_DEL_CANAL)
#         if canal:
#             try:
#                 contenido = obtener_reporte()
#                 await canal.send(embed=contenido) # type: ignore
#             except Exception as e:
#                 await canal.send(embed=alerta("reporte", e)) # type: ignore


@bot.command()
async def menu(ctx):
    embed = discord.Embed(
        title="**Menú:**",
        color=discord.Color.gold()
    )
    embed.description = f"- **!partidos:** Obtener partidos de la fecha actual y anterior.\n"
    embed.description+= f"- **!tabla:** Obtener la tabla de posiciones actual.\n"
    await ctx.send(embed=embed)


@bot.command()
async def partidos(ctx):
    try:
        embed = obtener_partidos()
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=alerta("partidos", e))


@bot.command()
async def tabla(ctx):
    try:
        embed = obtener_tabla()
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=alerta("tabla", e))


@bot.command()
async def test(ctx):
    try:
        await ctx.send("No hay nada que testear.")
    except Exception as e:
        await ctx.send(embed=alerta("test", e))



def alerta(nombre_funcion,e):
    embed = discord.Embed(
        title="⚠️ **ERROR**",
        description=f"**Se llevaron preso al Chiqui Tapia.**",
        color=discord.Color.orange()
    )
    print(nombre_funcion, e)
    return embed



bot.run(TOKEN_BOT) # type: ignore