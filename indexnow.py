#!/usr/bin/env python3
"""Avisa a Bing (y a Yandex, Seznam, Naver) de que el sitio ha cambiado.

IndexNow es un protocolo abierto: no hace falta cuenta ni verificacion en
Bing Webmaster Tools. Basta con publicar un fichero <clave>.txt en la raiz
del dominio y llamar a la API con esa clave.

Importa porque el indice de Bing es el que alimenta las respuestas de
ChatGPT Search y de Copilot: si Bing no ha rastreado un cambio, esos
asistentes siguen citando la version antigua.

Uso:
    python3 indexnow.py            # envia todas las URLs del sitemap
    python3 indexnow.py --dry-run  # muestra que enviaria, sin enviar
    python3 indexnow.py /carta /menu-del-dia    # solo esas rutas

Ejecutalo despues de cada despliegue con cambios de contenido.
"""
import glob
import json
import os
import re
import sys
import urllib.request

HOST = "www.smithersrestaurant.com"
BASE = "https://" + HOST
RAIZ = os.path.dirname(os.path.abspath(__file__))
API = "https://api.indexnow.org/indexnow"


def leer_clave():
    """La clave es el nombre del fichero <clave>.txt de la raiz del sitio."""
    for p in glob.glob(os.path.join(RAIZ, "*.txt")):
        nombre = os.path.basename(p)[:-4]
        if re.fullmatch(r"[0-9a-f]{8,128}", nombre):
            with open(p, encoding="utf-8") as f:
                if f.read().strip() == nombre:
                    return nombre
    sys.exit("No encuentro el fichero de clave IndexNow. "
             "Debe llamarse <clave>.txt y contener la clave.")


def urls_del_sitemap():
    with open(os.path.join(RAIZ, "sitemap.xml"), encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv

    clave = leer_clave()
    urls = [BASE + a if a.startswith("/") else a for a in args] or urls_del_sitemap()

    print(f"host:  {HOST}")
    print(f"clave: {clave}")
    print(f"URLs:  {len(urls)}")
    for u in urls:
        print("   ", u)

    if dry:
        print("\n--dry-run: no se ha enviado nada.")
        return

    cuerpo = json.dumps({
        "host": HOST,
        "key": clave,
        "keyLocation": f"{BASE}/{clave}.txt",
        "urlList": urls,
    }).encode("utf-8")

    req = urllib.request.Request(
        API, data=cuerpo,
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"\nRespuesta: {r.status} {r.reason}")
            # 200 = aceptado, 202 = aceptado pero la clave aun no se ha validado
            if r.status in (200, 202):
                print("Enviado correctamente.")
    except urllib.error.HTTPError as e:
        print(f"\nError {e.code}: {e.reason}")
        print(e.read().decode("utf-8", "replace")[:400])
        print("\n422 suele significar que el fichero de clave todavia no es "
              "accesible en el dominio: despliega primero, luego reintenta.")
        sys.exit(1)


if __name__ == "__main__":
    main()
