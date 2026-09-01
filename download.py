"""
Ejecuta este script UNA VEZ para descargar Blockly localmente.
Puede ser dandole click al botón ▶︎ de la derecha arriba
O ejecutando python download.py
"""
import urllib.request
import os
import sys

BASE = "https://cdnjs.cloudflare.com/ajax/libs/blockly/9.3.3"
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "crea_sesame_lib", "gui", "blockly")

# These are the REAL files — the *.min.js ones are just tiny module wrappers
FILES = {
    "blockly_compressed.js":        "blockly_compressed.js",
    "blocks_compressed.js":         "blocks_compressed.js",
    "python_compressed.js":         "python_compressed.js",
}

def main():
    os.makedirs(os.path.join(OUT, "msg"), exist_ok=True)

    for url_path, local_name in FILES.items():
        url  = f"{BASE}/{url_path}"
        dest = os.path.join(OUT, local_name)
        print(f"Descargando {url_path}...", end=" ", flush=True)
        try:
            urllib.request.urlretrieve(url, dest)
            size = os.path.getsize(dest)
            print(f"✓  ({size // 1024} KB)")
            if size < 10_000:
                print(f"  WARNING: Archivo sospechosamente pequeño ({size} bytes)")
                print(f"  Contenido: {open(dest).read()[:120]}")
        except Exception as e:
            print(f"\n✗  Error: {e}")
            sys.exit(1)

    print(f"\n✅ Blockly 9.3.3 descargado en:\n   {OUT}")
    print("Ya puedes ejecutar main.py para abrir el editor.")

if __name__ == "__main__":
    main()