# 🖥️ IAConsoleV2 – Interfaz de línea de comandos para GPT4All

Este script permite interactuar con modelos **GPT4All** directamente desde la terminal.  
Podrás listar modelos oficiales, consultar los que tienes instalados, desinstalar modelos, cambiar el modelo por defecto y enviar preguntas, todo sin salir de la consola.

---

## 📦 Requisitos
- **Python** 3.9 o superior  
- Dependencias:
  ```bash
  pip3 install -r requeriments.txt
  
## 📖 Instrucciones
 ```bash
python3 IAConsoleV2.py -h

 _______   _____     ___                              __         _     _    ____
(_______) (_____)  _(___)_         _      ____       (__)  ____ (_)   (_) _(____)
   (_)   (_)___(_)(_)   (_)  ___  (_)__  (____)  ___  (_) (____)(_)   (_)(_) _(_)
   (_)   (_______)(_)    _  (___) (____) (_)__  (___) (_)(_)_(_)(_)   (_)  _(_)
 __(_)__ (_)   (_)(_)___(_)(_)_(_)(_) (_) _(__)(_)_(_)(_)(__)__  (_)_(_)  (_)___
(_______)(_)   (_)  (___)   (___) (_) (_)(____) (___)(___)(____)  (___)  (______)
                                                                                                                                                                                         

usage: IAConsoleV2.py [-h] [--model MODEL] [--uninstall] [--list] [--list-installed] ...

💬 Chat con GPT4All desde terminal

positional arguments:
  pregunta          Pregunta o prompt para el modelo

options:
  -h, --help        show this help message and exit
  --model MODEL     Modelo a usar
  --uninstall       Eliminar el modelo actual y salir
  --list            Mostrar lista oficial de modelos GPT4All
  --list-installed  Mostrar modelos instalados en caché

