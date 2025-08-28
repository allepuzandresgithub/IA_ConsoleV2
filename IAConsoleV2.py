import sys
import os
import argparse
import requests
from bs4 import BeautifulSoup
from gpt4all import GPT4All
import threading
import itertools
import time
from colorama import init, Fore, Style
import argparse

init(autoreset=True)

BANNER = f"""{Fore.MAGENTA}
                                                                                  
 _______   _____     ___                              __         _     _    ____  
(_______) (_____)  _(___)_         _      ____       (__)  ____ (_)   (_) _(____) 
   (_)   (_)___(_)(_)   (_)  ___  (_)__  (____)  ___  (_) (____)(_)   (_)(_) _(_) 
   (_)   (_______)(_)    _  (___) (____) (_)__  (___) (_)(_)_(_)(_)   (_)  _(_)   
 __(_)__ (_)   (_)(_)___(_)(_)_(_)(_) (_) _(__)(_)_(_)(_)(__)__  (_)_(_)  (_)___  
(_______)(_)   (_)  (___)   (___) (_) (_)(____) (___)(___)(____)  (___)  (______) 
                                                                                                                                                                                                                                                                                                                            
{Style.RESET_ALL}"""

print(BANNER)

parser = argparse.ArgumentParser(description="💬 Chat con GPT4All desde terminal")
parser.add_argument("--model", default="mistral-7b-instruct-v0.1.Q4_0.gguf", help="Modelo a usar")
parser.add_argument("--uninstall", action="store_true", help="Eliminar el modelo actual y salir")
parser.add_argument("--list", action="store_true", help="Mostrar lista oficial de modelos GPT4All")
parser.add_argument("--list-installed", action="store_true", help="Mostrar modelos instalados en caché")
parser.add_argument("pregunta", nargs=argparse.REMAINDER, help="Pregunta o prompt para el modelo")
args = parser.parse_args()

model_name = args.model
cache_dir = os.path.expanduser("~/.cache/gpt4all")

# Spinner
def mostrar_spinner(mensaje, stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(f'\r{mensaje} {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(mensaje) + 2) + '\r')

if args.list:
    url = "https://docs.gpt4all.io/gpt4all_desktop/models.html"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        tables = soup.find_all("table")
        if not tables:
            print("⚠️ No se encontró la tabla de modelos en la página.")
        else:
            print("🌐 Modelos oficiales GPT4All disponibles:\n")
            rows = tables[0].find_all("tr")
            for i, row in enumerate(rows):
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if i == 0:
                    print(" | ".join(cols))
                    print("-" * 80)
                else:
                    print(" | ".join(cols))
    except Exception as e:
        print(f"⚠️ Error al obtener la lista: {e}")
    sys.exit(0)

if args.list_installed:
    if os.path.exists(cache_dir):
        modelos = [f for f in os.listdir(cache_dir) if f.endswith(".gguf")]
        if modelos:
            print("📂 Modelos instalados en caché:\n")
            for m in modelos:
                print(f" - {m}")
        else:
            print("ℹ️ No hay modelos instalados.")
    else:
        print("ℹ️ No existe la carpeta de caché.")
    sys.exit(0)

if args.uninstall:
    model_path = os.path.join(cache_dir, model_name)
    if os.path.exists(model_path):
        os.remove(model_path)
        print(f"✅ Modelo '{model_name}' eliminado del caché")
    else:
        print(f"ℹ️ No se encontró el modelo '{model_name}' en {cache_dir}")
    sys.exit(0)

if not args.pregunta:
    parser.print_usage()
    sys.exit(1)

pregunta = " ".join(args.pregunta)

try:
    model = GPT4All(model_name, device="cpu")

    stop_spinner = threading.Event()
    hilo_spinner = threading.Thread(target=mostrar_spinner, args=("Procesando solicitud", stop_spinner))
    hilo_spinner.start()

    with model.chat_session():
        respuesta = model.generate(pregunta, max_tokens=500)

    stop_spinner.set()
    hilo_spinner.join()

    print("\n💬 Respuesta:")
    print(respuesta)

except Exception as e:
    stop_spinner.set()
    print(f"\n⚠️ Error: {e}")

