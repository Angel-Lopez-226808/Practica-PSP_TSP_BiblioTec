"""MÓDULO LIBROS — Integrante A.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un libro:
    {"id": 1, "titulo": "...", "autor": "...", "isbn": "9780307474728",
     "anio": 1967, "categoria": "Novela", "disponible": True}

Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import (
    ANIO_MINIMO, CAMPOS_EDITABLES_LIBRO, CATEGORIAS, LONGITUD_ISBN, ORDENES_LIBRO,
)
from nucleo.utilidades import hoy_o, normalizar, solo_digitos


def listar_libros(repo):
    """Actividad 1 · Día 1 — Listar libros.

    Regresa todos los libros ordenados por título (sin importar
    mayúsculas ni acentos; usa normalizar()).
    A cada libro le agrega la llave "estado" con el texto
    "Disponible" si disponible es True, o "Prestado" si es False.
    """
    # TODO: implementar (Actividad 1 · Día 1)
    raise NotImplementedError("Actividad 1 pendiente")


def agregar_libro(repo, titulo, autor, isbn, anio, categoria, hoy=None):
    """Actividad 2 · Día 1 — Agregar libro con validación.

    Reglas (si alguna falla, lanza ValueError):
      - titulo y autor no pueden quedar vacíos (después de quitar espacios).
      - isbn: se le quitan guiones y espacios (solo_digitos); debe quedar con
        exactamente 13 dígitos numéricos.
      - No puede existir otro libro con el mismo isbn.
      - anio: entero entre ANIO_MINIMO (1450) y el año de `hoy`, inclusive.
        Puede llegar como texto ("1990"); conviértelo a int. Si no es un
        número, también es ValueError.
      - categoria: debe estar en CATEGORIAS.
    Guarda el libro con titulo y autor sin espacios en los extremos,
    el isbn limpio, anio como int y "disponible": True.
    Regresa el id asignado.
    """
    # TODO: implementar (Actividad 2 · Día 1)
    raise NotImplementedError("Actividad 2 pendiente")


def buscar_libros(repo, texto):
    """Actividad 3 · Día 2 — Buscar libros.

    Regresa los libros cuyo título O autor contengan `texto`, sin importar
    mayúsculas ni acentos ("garcia" encuentra "García Márquez").
    Si texto está vacío o solo tiene espacios, regresa todos los libros.
    El resultado va ordenado por título (normalizado), igual que listar_libros,
    y cada libro lleva también la llave "estado".
    """
    # TODO: implementar (Actividad 3 · Día 2)
    raise NotImplementedError("Actividad 3 pendiente")


def editar_libro(repo, libro_id, cambios, hoy=None):
    """Actividad 4 · Día 2 — Editar libro.

    `cambios` es un dict, por ejemplo {"titulo": "Nuevo", "anio": "2001"}.
      - Si el libro no existe -> ValueError.
      - Solo se pueden cambiar los campos de CAMPOS_EDITABLES_LIBRO
        (titulo, autor, anio, categoria). Cualquier otro campo (por ejemplo
        "isbn" o "disponible") -> ValueError.
      - Los valores se validan con las mismas reglas de agregar_libro:
        titulo/autor no vacíos (se guardan sin espacios extra),
        anio entero en rango, categoria válida.
    Regresa el libro actualizado (el dict que regresa repo.actualizar).
    """
    # TODO: implementar (Actividad 4 · Día 2)
    raise NotImplementedError("Actividad 4 pendiente")


def eliminar_libro(repo, libro_id):
    """Actividad 5 · Día 3 — Eliminar libro.

      - Si el libro no existe -> ValueError.
      - Si el libro tiene un préstamo activo (un registro en "prestamos" con
        ese libro_id y fecha_devolucion None) -> ValueError.
      - Si tiene préstamos ya devueltos, sí se puede eliminar.
    Regresa True cuando se elimina.
    """
    # TODO: implementar (Actividad 5 · Día 3)
    raise NotImplementedError("Actividad 5 pendiente")


def libros_por_categoria(repo, categoria=None, orden="titulo"):
    """Actividad 6 · Día 3 — Filtrar por categoría y ordenar.

      - categoria: si es None o "", no filtra; si tiene valor, debe estar en
        CATEGORIAS (si no -> ValueError) y solo regresa esos libros.
      - orden: uno de ORDENES_LIBRO ("titulo", "autor", "anio");
        cualquier otro -> ValueError.
          "titulo" y "autor": orden alfabético normalizado.
          "anio": del más reciente al más antiguo; si empatan, por título.
    Cada libro lleva también la llave "estado" (como en listar_libros).
    """
    # TODO: implementar (Actividad 6 · Día 3)
    raise NotImplementedError("Actividad 6 pendiente")
