import json
from pathlib import Path

ARCHIVO = Path(__file__).parent / "datos" / "libros.json"
ultimo_id = 0


def cargar_libros():
    global ultimo_id
    if not ARCHIVO.exists():
        return []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            libros = json.load(f)
    except Exception:
        return []

    if libros:
        mayor = max(l["id"] for l in libros)
        if mayor > ultimo_id:
            ultimo_id = mayor
    return sorted(libros, key=lambda l: l["id"])


def guardar_libros(libros):
    ARCHIVO.parent.mkdir(parents=True, exist_ok=True)
    libros_ordenados = sorted(libros, key=lambda l: l["id"])
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(libros_ordenados, f, indent=4, ensure_ascii=False)


def siguiente_id():
    global ultimo_id
    cargar_libros()
    ultimo_id += 1
    return ultimo_id
