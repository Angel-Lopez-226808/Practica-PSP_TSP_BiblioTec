"""Pruebas del módulo LIBROS. NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

import pytest

from nucleo.utilidades import normalizar
from modulos.libros import (
    agregar_libro, buscar_libros, editar_libro, eliminar_libro, libros_por_categoria, listar_libros,
)


def ids(libros):
    return [l["id"] for l in libros]


# ------------------------------------------------------------ Actividad 1
def test_f1_regresa_todos_los_libros(repo):
    assert len(listar_libros(repo)) == 12, "Debe regresar los 12 libros de ejemplo"


def test_f1_ordenados_por_titulo_sin_acentos(repo):
    titulos = [l["titulo"] for l in listar_libros(repo)]
    assert titulos[0] == "Breve historia del tiempo", "El primero debe ser 'Breve historia del tiempo'"
    assert titulos[2] == "Código limpio", "'Código limpio' va antes de 'Como agua para chocolate' (orden sin acentos)"
    assert titulos[-1] == "Visión de los vencidos", "El último debe ser 'Visión de los vencidos'"


def test_f1_agrega_llave_estado(repo):
    por_id = {l["id"]: l for l in listar_libros(repo)}
    assert por_id[1]["estado"] == "Prestado", "Un libro no disponible debe tener estado 'Prestado'"
    assert por_id[2]["estado"] == "Disponible", "Un libro disponible debe tener estado 'Disponible'"


def test_f1_conserva_los_datos_originales(repo):
    libro = next(l for l in listar_libros(repo) if l["id"] == 4)
    assert libro["isbn"] == "9788420671123" and libro["disponible"] is True, "No debe alterar los campos del libro"


# ------------------------------------------------------------ Actividad 2
def test_f2_agrega_y_regresa_id(repo, hoy):
    nuevo_id = agregar_libro(repo, "Aura", "Carlos Fuentes", "9786073141286", 1962, "Novela", hoy)
    assert nuevo_id == 13, "Debe regresar el id que asigna repo.agregar()"
    libro = repo.obtener("libros", nuevo_id)
    assert libro is not None, "El libro no se guardó en el repositorio"
    assert libro["disponible"] is True, "Un libro nuevo debe quedar disponible"


def test_f2_limpia_isbn_titulo_y_anio(repo, hoy):
    nuevo_id = agregar_libro(repo, "  Aura ", " Carlos Fuentes  ", "978-607-314 1286", "1962", "Novela", hoy)
    libro = repo.obtener("libros", nuevo_id)
    assert libro["isbn"] == "9786073141286", "El ISBN debe guardarse sin guiones ni espacios"
    assert libro["titulo"] == "Aura" and libro["autor"] == "Carlos Fuentes", "Título y autor sin espacios extra"
    assert libro["anio"] == 1962, "El año debe guardarse como entero"


@pytest.mark.parametrize("isbn", ["978607314128", "97860731412861", "97860731412AB", ""])
def test_f2_isbn_invalido(repo, hoy, isbn):
    with pytest.raises(ValueError):
        agregar_libro(repo, "Aura", "Carlos Fuentes", isbn, 1962, "Novela", hoy)


def test_f2_isbn_duplicado(repo, hoy):
    with pytest.raises(ValueError):
        agregar_libro(repo, "Otro", "Alguien", "978-0307474728", 2000, "Novela", hoy)


@pytest.mark.parametrize("anio", [1449, 2027, "abc", None])
def test_f2_anio_invalido(repo, hoy, anio):
    with pytest.raises(ValueError):
        agregar_libro(repo, "Aura", "Carlos Fuentes", "9786073141286", anio, "Novela", hoy)


def test_f2_limites_de_anio_validos(repo, hoy):
    agregar_libro(repo, "Antiguo", "Anónimo", "1111111111111", 1450, "Historia", hoy)
    agregar_libro(repo, "Reciente", "Autora", "2222222222222", 2026, "Ciencia", hoy)
    assert len(repo.listar("libros")) == 14, "1450 y el año actual son años válidos"


@pytest.mark.parametrize("titulo, autor, categoria", [
    ("   ", "Carlos Fuentes", "Novela"),
    ("Aura", "", "Novela"),
    ("Aura", "Carlos Fuentes", "Poesía"),
])
def test_f2_campos_obligatorios_y_categoria(repo, hoy, titulo, autor, categoria):
    with pytest.raises(ValueError):
        agregar_libro(repo, titulo, autor, "9786073141286", 1962, categoria, hoy)


# ------------------------------------------------------------ Actividad 3
def test_f3_busca_por_autor_sin_acentos(repo):
    assert ids(buscar_libros(repo, "garcia")) == [1], "'garcia' debe encontrar a García Márquez"
    assert ids(buscar_libros(repo, "RULFO")) == [2], "La búsqueda no distingue mayúsculas"


def test_f3_busca_por_titulo(repo):
    assert ids(buscar_libros(repo, "tiempo")) == [3]
    assert ids(buscar_libros(repo, "codigo")) == [7], "'codigo' debe encontrar 'Código limpio'"


def test_f3_texto_vacio_regresa_todos(repo):
    assert len(buscar_libros(repo, "")) == 12
    assert len(buscar_libros(repo, "   ")) == 12, "Solo espacios cuenta como texto vacío"


def test_f3_ordenado_y_con_estado(repo):
    resultado = buscar_libros(repo, "el")
    titulos = [l["titulo"] for l in resultado]
    assert titulos == sorted(titulos, key=normalizar), "Debe ir ordenado por título"
    assert all("estado" in l for l in resultado), "Cada libro debe traer la llave 'estado'"


def test_f3_sin_resultados(repo):
    assert buscar_libros(repo, "zzz") == []


# ------------------------------------------------------------ Actividad 4
def test_f4_edita_y_limpia_valores(repo, hoy):
    libro = editar_libro(repo, 2, {"titulo": " Pedro Páramo (edición especial) ", "anio": "1956"}, hoy)
    assert libro["titulo"] == "Pedro Páramo (edición especial)", "El título debe guardarse sin espacios extra"
    assert libro["anio"] == 1956, "El año debe guardarse como entero"
    assert repo.obtener("libros", 2)["anio"] == 1956, "El cambio debe quedar guardado en el repositorio"


def test_f4_no_cambia_otros_campos(repo, hoy):
    editar_libro(repo, 2, {"categoria": "Historia"}, hoy)
    libro = repo.obtener("libros", 2)
    assert libro["autor"] == "Juan Rulfo" and libro["isbn"] == "9786071603579"


def test_f4_libro_inexistente(repo, hoy):
    with pytest.raises(ValueError):
        editar_libro(repo, 99, {"titulo": "X"}, hoy)


@pytest.mark.parametrize("cambios", [{"isbn": "1234567890123"}, {"disponible": False}])
def test_f4_campo_no_editable(repo, hoy, cambios):
    with pytest.raises(ValueError):
        editar_libro(repo, 2, cambios, hoy)


@pytest.mark.parametrize("cambios", [{"anio": 3000}, {"anio": "x"}, {"categoria": "Poesía"}, {"titulo": " "}])
def test_f4_valida_valores(repo, hoy, cambios):
    with pytest.raises(ValueError):
        editar_libro(repo, 2, cambios, hoy)
    assert repo.obtener("libros", 2)["titulo"] == "Pedro Páramo", "Si hay error no debe guardar nada"


# ------------------------------------------------------------ Actividad 5
def test_f5_elimina_libro_disponible(repo):
    assert eliminar_libro(repo, 2) is True
    assert repo.obtener("libros", 2) is None, "El libro debe desaparecer del repositorio"


def test_f5_no_elimina_libro_prestado(repo):
    with pytest.raises(ValueError):
        eliminar_libro(repo, 3)
    assert repo.obtener("libros", 3) is not None, "Un libro prestado no debe eliminarse"


def test_f5_libro_con_prestamos_devueltos_si_se_elimina(repo):
    # El libro 7 tiene un préstamo devuelto y uno activo; devolvemos el activo.
    repo.actualizar("prestamos", 5, {"fecha_devolucion": "2026-10-15"})
    repo.actualizar("libros", 7, {"disponible": True})
    assert eliminar_libro(repo, 7) is True, "Los préstamos ya devueltos no impiden eliminar"


def test_f5_libro_inexistente(repo):
    with pytest.raises(ValueError):
        eliminar_libro(repo, 99)


# ------------------------------------------------------------ Actividad 6
def test_f6_filtra_por_categoria(repo):
    assert sorted(ids(libros_por_categoria(repo, "Tecnología"))) == [7, 8, 9]


def test_f6_sin_categoria_regresa_todos(repo):
    assert len(libros_por_categoria(repo)) == 12
    assert len(libros_por_categoria(repo, "")) == 12


def test_f6_orden_por_anio_descendente(repo):
    resultado = libros_por_categoria(repo, None, "anio")
    assert resultado[0]["titulo"] == "Sapiens", "El más reciente (2011) va primero"
    empate = [l["titulo"] for l in resultado if l["anio"] == 1988]
    assert empate == ["Breve historia del tiempo", "Matilda"], "Si empatan en año, se ordenan por título"


def test_f6_orden_por_autor(repo):
    assert ids(libros_por_categoria(repo, "Novela", "autor")) == [1, 2, 12]


def test_f6_orden_por_titulo_es_el_predeterminado(repo):
    assert ids(libros_por_categoria(repo, "Ciencia")) == [3, 4]


@pytest.mark.parametrize("categoria, orden", [("Poesía", "titulo"), ("Novela", "precio")])
def test_f6_valores_invalidos(repo, categoria, orden):
    with pytest.raises(ValueError):
        libros_por_categoria(repo, categoria, orden)


def test_f6_incluye_estado(repo):
    assert all("estado" in l for l in libros_por_categoria(repo, "Infantil"))
