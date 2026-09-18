import discord, time, undetected_chromedriver as uc
from bs4 import BeautifulSoup # beautifulsoup4

# # Hacer clic: elemento.click() (Es como tocar la pantalla con el dedito).
# # Escribir: elemento.send_keys("hola") (Como tipear en el teclado).
# # Borrar texto: elemento.clear() (Pasa una goma de borrar invisible si la caja ya tenía texto escrito).
# robot = uc.Chrome()

# # NAVEGAR
# robot.get("https://www.google.com/search?q=liga+argentina+partidos&oq=liga+&gs_lcrp=EgZjaHJvbWUqCAgAEEUYJxg7MggIABBFGCcYOzIGCAEQRRg5MgoIAhAuGLEDGIAEMg0IAxAuGIMBGLEDGIAEMhAIBBAuGIMBGLEDGIAEGLQHMgoIBRAuGLEDGIAEMgcIBhAAGIAEMgcIBxAAGIAEMgoICBAuGLEDGIAEMhAICRAuGIMBGLEDGIAEGIoF0gEIMzM1OGowajSoAgCwAgA&sourceid=chrome&source=chrome.ob&ie=UTF-8#sie=lg;/g/11msmq3ggx;2;/m/04hpk1;mt;fp;1;;;;-1")

# # Esperamos hasta q vea la página
# time.sleep(15)

# with open("liga.html", "w", encoding="utf-8") as archivo:
#     archivo.write(robot.page_source)

# sopa = BeautifulSoup(robot.page_source, "html.parser")

# with open("liga_sopa.html", "w", encoding="utf-8") as archivo:
#     archivo.write(sopa.prettify()) # type: ignore


def obtener_reporte():
    with open("liga_sopa.html", "r", encoding="utf-8") as archivo:
        sopa_html = archivo.read()

    sopa = BeautifulSoup(sopa_html, "html.parser")

    textos = list(sopa.stripped_strings)

    for i in range(len(textos) - 1, -1, -1):
        if "►" in textos[i]:
            del textos[i]
            
    #imagenes = [imagen.get('src') for imagen in sopa.find_all('img') if imagen.get('src')]

    finalizados = {}
    proximos = {}
    for i in range(len(textos)):
        if "jornada" in textos[i].lower() and "fin" in textos[i+1].lower():
            finalizados["jornada"] = textos[i]
            finalizados["partidos"] = []
            for j in range(15):
                finalizados["partidos"].append(
                    {
                        "estado": textos[i+1 + 8*j],
                        "fecha": textos[i+2 + 8*j], 
                        "equipos": [
                            {"nombre": textos[i+3 + 8*j], "resultado":textos[i+5 + 8*j]},
                            {"nombre": textos[i+6 + 8*j], "resultado":textos[i+8 + 8*j]}
                        ]
                    }
                )

        elif "jornada" in textos[i].lower() and "fin" not in textos[i+1].lower():
            proximos["jornada"] = textos[i]
            proximos["partidos"] = []
            for j in range(15):
                fecha = textos[i+2 + 6*j].split()
                proximos["partidos"].append(
                    {   
                        "estado": textos[i+1 + 6*j],
                        "fecha": f"{fecha[0]} {fecha[1][0]}{fecha[2][0]}",
                        "equipos": [
                            {"nombre": textos[i+3 + 6*j]},
                            {"nombre": textos[i+5 + 6*j]}
                        ]
                    }
                )
            break
        
    # print("\n")
    # print(datos_finalizados, "\n\n")
    # print(datos_no_iniciados)
    
    embed = discord.Embed(
        title="⚽ El Chiqui Tapia trajo el resumen:", 
        color=discord.Color.blue()
    )

    def agregar_jornada(datos):
        lista_partidos = []
        
        for p in datos['partidos']:
            eq1 = p['equipos'][0]['nombre']
            eq2 = p['equipos'][1]['nombre']
            
            if p.get('estado') == 'Fin':
                info = f"` {p['equipos'][0]['resultado']} - {p['equipos'][1]['resultado']} `"
            else:
                info = f"` {p['estado']} {p['fecha']} `"
            
            lista_partidos.append(f"• **{eq1}** {info} **{eq2}**")
        
        # Agregamos toda la jornada en un único bloque de arriba a abajo (inline=False)
        embed.add_field(
            name=f"🏆 {datos['jornada']}", 
            value="\n".join(lista_partidos), 
            inline=False
        )
        
    agregar_jornada(finalizados)
    agregar_jornada(proximos)
    
    return embed