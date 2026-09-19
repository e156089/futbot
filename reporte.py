import discord, time, json, os, undetected_chromedriver as uc
from datetime import datetime
from bs4 import BeautifulSoup # beautifulsoup4

# sudo apt-get update
# sudo apt-get install xvfb

def buscar_info(URL):
    # Hacer clic: elemento.click() (Es como tocar la pantalla con el dedito).
    # Escribir: elemento.send_keys("hola") (Como tipear en el teclado).
    # Borrar texto: elemento.clear() (Pasa una goma de borrar invisible si la caja ya tenía texto escrito).
    robot = uc.Chrome()
    # NAVEGAR
    robot.get(URL)
    time.sleep(10) # Esperar q cargue la página
    sopa = BeautifulSoup(robot.page_source, "html.parser") # Obtener html
    robot.quit()
    textos_html = list(sopa.stripped_strings)
    
    return textos_html # Lista de textos html
    

def crear_diccionario(textos_html):
    for i in range(len(textos_html) - 1, -1, -1):
        if "►" in textos_html[i] or textos_html[i] == textos_html[i-1]:
            del textos_html[i]

    cont = 0
    for i in range(len(textos_html)):
        if "jornada" in textos_html[i].lower():
            cont += 1
            if cont == 2:
                textos_html = textos_html[i:]
                break

    finalizados = {}
    proximos = {}
    ind_f = 6
    ind_p = 4
    # print(textos_html)
    for i in range(len(textos_html)):
        if "jornada" in textos_html[i].lower() and "fin" in textos_html[i+1].lower() and "fin" in textos_html[i+1 + ind_f*14].lower():
            finalizados["jornada"] = textos_html[i]
            finalizados["partidos"] = []
            for j in range(15):
                ind = ind_f*j
                finalizados["partidos"].append(
                    {
                        "estado": textos_html[i+1 + ind],
                        "fecha": textos_html[i+2 + ind].replace("/", "-"), 
                        "equipos": [
                            {"nombre": textos_html[i+3 + ind], "resultado":textos_html[i+4 + ind]},
                            {"nombre": textos_html[i+5 + ind], "resultado":textos_html[i+6 + ind]}
                        ]
                    }
                )

        elif "jornada" in textos_html[i].lower():
            proximos["jornada"] = textos_html[i]
            proximos["partidos"] = []
            cal = 0 # calibracion de indice
            for j in range(15):
                ind_add = ind_p*j+cal
                if "fin" in textos_html[i+1 + ind_add].lower():
                    proximos["partidos"].append(
                        {
                            "estado": textos_html[i+1 + ind_add],
                            "fecha": textos_html[i+2 + ind_add].replace("/", "-"), 
                            "equipos": [
                                {"nombre": textos_html[i+3 + ind_add], "resultado":textos_html[i+4 + ind_add]},
                                {"nombre": textos_html[i+5 + ind_add], "resultado":textos_html[i+6 + ind_add]}
                            ]
                        }
                    )
                    cal += 2
                elif "vivo" in textos_html[i+1 + ind_add].lower():
                    proximos["partidos"].append(
                        {
                            "estado": f"{textos_html[i+1 + ind_add]} {textos_html[i+2 + ind_add]}{textos_html[i+3 + ind_add]}",
                            "fecha": None, 
                            "equipos": [
                                {"nombre": textos_html[i+4 + ind_add], "resultado":textos_html[i+5 + ind_add]},
                                {"nombre": textos_html[i+6 + ind_add], "resultado":textos_html[i+7 + ind_add]}
                            ]
                        }
                    )
                    cal += 3
                elif "entretiempo" in textos_html[i+1 + ind_add].lower():
                    proximos["partidos"].append(
                        {
                            "estado": textos_html[i+1 + ind_add],
                            "fecha": None, 
                            "equipos": [
                                {"nombre": textos_html[i+2 + ind_add], "resultado":textos_html[i+3 + ind_add]},
                                {"nombre": textos_html[i+4 + ind_add], "resultado":textos_html[i+5 + ind_add]}
                            ]
                        }
                    )
                    cal += 1
                else:
                    fecha = textos_html[i+2 + ind_add].split()
                    ultima_fecha = textos_html[i+1 + ind_add].split()
                    proximos["partidos"].append(
                        {   
                            "estado": "Proximamente",
                            "fecha": f"{textos_html[i+1 + ind_add]} {fecha[0]} {fecha[1][0]}{fecha[2][0]}",
                            "equipos": [
                                {"nombre": textos_html[i+3 + ind_add]},
                                {"nombre": textos_html[i+4 + ind_add]}
                            ]
                        }
                    )
            break
    # print("\n")
    # print(finalizados, "\n\n")
    # print(proximos)
    return {"finalizados": finalizados, "proximos": proximos}


def crear_embed(contenido):
    embed = discord.Embed(
        title="⚽ El Chiqui Tapia trajo el resumen:", 
        color=discord.Color.blue()
    )

    def agregar_jornada(datos):
        lista_partidos = []
        
        for p in datos['partidos']:
            eq1 = p['equipos'][0]['nombre']
            eq2 = p['equipos'][1]['nombre']
            
            if "fin" in p.get('estado').lower():
                info = f"` {p['equipos'][0]['resultado']} - {p['equipos'][1]['resultado']} `"
            elif "vivo" in p.get('estado').lower():
                eq1 = f"{p.get("estado")}:  {eq1}"
                info = f"` {p['equipos'][0]['resultado']} - {p['equipos'][1]['resultado']} `"
            elif "entretiempo" in p.get('estado').lower():
                eq1 = f"{p.get("estado")}:  {eq1}"
                info = f"` {p['equipos'][0]['resultado']} - {p['equipos'][1]['resultado']} `"
            else:
                info = f"` {p['fecha']} `"
            
            lista_partidos.append(f"• **{eq1}** {info} **{eq2}**")
        
        # Agregamos toda la jornada en un único bloque de arriba a abajo (inline=False)
        embed.add_field(
            name=f"\n🏆 {datos['jornada']}", 
            value="\n".join(lista_partidos), 
            inline=False
        )
        
    agregar_jornada(contenido["finalizados"])
    agregar_jornada(contenido["proximos"])
    
    return embed


def obtener_partidos():

    # info_actualizada = False
    # path = "liga_partidos.json"
    # if os.path.isfile(path):
    #     with open(path, "r", encoding="utf-8") as archivo:
    #         contenido = json.load(archivo)

    #     fecha = contenido["fecha"].strip()
    #     fecha_guardada = datetime.strptime(fecha, "%Y-%m-%d").date()
    #     hoy = datetime.now().date()

    #     if fecha_guardada > hoy:
    #         info_actualizada = True

    # if not info_actualizada:
    URL = "https://www.google.com/search?q=liga+argentina+partidos&oq=liga+&gs_lcrp=EgZjaHJvbWUqCAgAEEUYJxg7MggIABBFGCcYOzIGCAEQRRg5MgoIAhAuGLEDGIAEMg0IAxAuGIMBGLEDGIAEMhAIBBAuGIMBGLEDGIAEGLQHMgoIBRAuGLEDGIAEMgcIBhAAGIAEMgcIBxAAGIAEMgoICBAuGLEDGIAEMhAICRAuGIMBGLEDGIAEGIoF0gEIMzM1OGowajSoAgCwAgA&sourceid=chrome&source=chrome.ob&ie=UTF-8#sie=lg;/g/11msmq3ggx;2;/m/04hpk1;mt;fp;1;;;;-1"
    textos_html = buscar_info(URL)
    contenido = crear_diccionario(textos_html)

        # with open(path, "w", encoding="utf-8") as archivo:
        #     json.dump(contenido, archivo)
            
    embed = crear_embed(contenido)
    return embed


def obtener_tabla():
    URL = "https://www.google.com/search?q=partidos+liga+argentina&oq=part&gs_lcrp=EgZjaHJvbWUqBggBECMYJzIGCAAQRRg5MgYIARAjGCcyBggCECMYJzIHCAMQABiABDIHCAQQABiABDIGCAUQRRg9MgYIBhBFGD0yBggHEEUYPNIBCDM4MjhqMGo3qAIIsAIB8QUH3g9qWDYsI_EFB94Palg2LCM&sourceid=chrome&source=chrome.ob&ie=UTF-8#sie=lg;/g/11msmq3ggx;2;/m/04hpk1;st;fp;1;;;;-1"