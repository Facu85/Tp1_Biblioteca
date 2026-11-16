from typing import Optional
from fastapi import FastAPI, HTTPException, Response
from datos import cargar_libros, guardar_libros, siguiente_id
from schemas import Libro, LibroParcial

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}


@app.get("/libros")
def obtener_libros(
    autor: Optional[str] = None,
    disponible: Optional[bool] = None,
    desde: int = 0,
    limite: int = 100,
):
    libros = cargar_libros()
    if autor is not None:
        libros = [l for l in libros if l["autor"].lower() == autor.lower()]
    if disponible is not None:
        libros = [l for l in libros if l["disponible"] == disponible]
    libros = libros[desde:]
    libros = libros[:limite]
    return libros


@app.get("/libros/buscar")
def buscar_libros(texto: str):
    libros = cargar_libros()
    t = texto.lower()
    return [
        l for l in libros
        if t in l["titulo"].lower() or t in l["autor"].lower()
    ]


@app.post("/libros", status_code=201)
def crear_libro(libro: Libro):
    libros = cargar_libros()
    for l in libros:
        if l["titulo"].lower() == libro.titulo.lower() and l["autor"].lower() == libro.autor.lower():
            raise HTTPException(status_code=409, detail="El libro ya existe")
    nuevo = {"id": siguiente_id(), **libro.model_dump()}
    libros.append(nuevo)
    guardar_libros(libros)
    return nuevo


@app.get("/libros/{id}")
def obtener_libro(id: int):
    for libro in cargar_libros():
        if libro["id"] == id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.put("/libros/{id}")
def reemplazar_libro(id: int, datos: Libro):
    libros = cargar_libros()
    for i, libro in enumerate(libros):
        if libro["id"] == id:
            libros[i] = {"id": id, **datos.model_dump()}
            guardar_libros(libros)
            return libros[i]
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.patch("/libros/{id}")
def actualizar_libro_parcial(id: int, datos: LibroParcial):
    libros = cargar_libros()
    for i, libro in enumerate(libros):
        if libro["id"] == id:
            cambios = datos.model_dump(exclude_unset=True)
            libros[i] = {**libro, **cambios}
            guardar_libros(libros)
            return libros[i]
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/libros/{id}", status_code=204)
def eliminar_libro(id: int):
    libros = cargar_libros()
    for libro in libros:
        if libro["id"] == id:
            libros.remove(libro)
            guardar_libros(libros)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Libro no encontrado")
