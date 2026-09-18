import discord, os, datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

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

    if not reporte.is_running(): # Empezar loop
        reporte.start()


hora = datetime.time(hour=0, minute=0)
@tasks.loop(time=hora)
async def reporte():
    hoy = datetime.datetime.now()
    # 0 = Lunes | 1 = Martes | 2 = Miércoles | 3 = Jueves 
    # 4 = Viernes | 5 = Sábado | 6 = Domingo
    if hoy.weekday() == 1:
        ID_DEL_CANAL = 1398376928716652697
        canal = bot.get_channel(ID_DEL_CANAL)
        if canal:
            try:
                from reporte import obtener_reporte
                contenido = obtener_reporte()
                await canal.send(embed=contenido) # type: ignore
            except Exception as e:
                await canal.send(embed=alerta("reporte", e)) # type: ignore


@bot.command()
async def menu(ctx):
    await ctx.send('Aca va a ir el futuro menu.\n**Madison**')



@bot.command()
async def test(ctx):
    try:
        ctx.send("No hay nada que testear.")
    except Exception as e:
        await ctx.send(embed=alerta("test", e))



def alerta(nombre_funcion,e):
    embed = discord.Embed(
        title="⚠️ **ERROR**",
        description=f"**Se llevaron preso al Chiqui Tapia.**\nFuncion -> {nombre_funcion}",
        color=discord.Color.orange()
    )
    print(nombre_funcion, e)
    return embed



bot.run(TOKEN_BOT) # type: ignore