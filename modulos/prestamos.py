"""MÓDULO PRÉSTAMOS — Integrante C.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un préstamo:
    {"id": 1, "libro_id": 3, "socio_id": 1, "fecha_prestamo": "2026-10-10",
     "fecha_limite": "2026-10-17", "fecha_devolucion": None, "multa": 0.0}

Las fechas se guardan como texto "AAAA-MM-DD"; usa a_fecha() para
convertirlas a date y poder compararlas o restarlas.
Un préstamo está ACTIVO si su fecha_devolucion es None.
Para errores de validación lanza ValueError("mensaje claro").
"""

from collections import Counter
from datetime import timedelta

from nucleo.config import DIAS_PRESTAMO, MAX_PRESTAMOS_ACTIVOS, MULTA_POR_DIA
from nucleo.utilidades import a_fecha, hoy_o, normalizar


def listar_prestamos_activos(repo):
    """Actividad 1 · Día 1 — Listar préstamos activos.

    Regresa los préstamos con fecha_devolucion None, ordenados por
    fecha_limite (la más próxima primero; si empatan, por id).
    A cada préstamo le agrega dos llaves:
      "titulo": el título del libro prestado
      "socio":  el nombre del socio
    """
    # TODO: implementar (Actividad 1 · Día 1)
    raise NotImplementedError("Actividad 1 pendiente")


def registrar_prestamo(repo, libro_id, socio_id, hoy=None):
    """Actividad 2 · Día 1 — Registrar préstamo.

    Reglas (si alguna falla, lanza ValueError):
      - El libro debe existir y tener disponible True.
      - El socio debe existir y tener activo True.
      - El socio debe tener MENOS de MAX_PRESTAMOS_ACTIVOS (3) préstamos activos.
    Crea el préstamo con:
      fecha_prestamo = hoy, fecha_limite = hoy + DIAS_PRESTAMO (7) días,
      fecha_devolucion = None, multa = 0.0   (fechas en formato "AAAA-MM-DD")
    y marca el libro con disponible False (repo.actualizar).
    Regresa el id del préstamo.
    """
    # TODO: implementar (Actividad 2 · Día 1)
    raise NotImplementedError("Actividad 2 pendiente")


def calcular_multa(fecha_limite, fecha_devolucion):
    """Actividad 3 · Día 2 — Calcular multa.

    Recibe dos fechas (date o texto "AAAA-MM-DD").
    Si la devolución es después de la fecha límite, la multa es
    MULTA_POR_DIA (5.0) por cada día de retraso. Si se devuelve
    a tiempo o antes, la multa es 0.0.
    Regresa un float.   calcular_multa("2026-10-10", "2026-10-13") -> 15.0
    """
    # TODO: implementar (Actividad 3 · Día 2)
    raise NotImplementedError("Actividad 3 pendiente")


def registrar_devolucion(repo, prestamo_id, hoy=None):
    """Actividad 4 · Día 2 — Registrar devolución.

      - Si el préstamo no existe -> ValueError.
      - Si ya fue devuelto (fecha_devolucion distinta de None) -> ValueError.
    Actualiza el préstamo con fecha_devolucion = hoy ("AAAA-MM-DD") y
    multa = calcular_multa(fecha_limite, hoy).
    Marca el libro con disponible True.
    Regresa la multa (float).
    """
    # TODO: implementar (Actividad 4 · Día 2)
    raise NotImplementedError("Actividad 4 pendiente")


def prestamos_vencidos(repo, hoy=None):
    """Actividad 5 · Día 3 — Listar préstamos vencidos.

    Regresa los préstamos ACTIVOS cuya fecha_limite es anterior a `hoy`.
    A cada uno le agrega:
      "titulo", "socio"      (igual que listar_prestamos_activos)
      "dias_retraso":        días entre fecha_limite y hoy (int)
      "multa_estimada":      calcular_multa(fecha_limite, hoy)
    Ordenados por dias_retraso, del mayor al menor (si empatan, por id).
    """
    # TODO: implementar (Actividad 5 · Día 3)
    raise NotImplementedError("Actividad 5 pendiente")


def reporte_prestamos(repo, top=3):
    """Actividad 6 · Día 3 — Reporte resumen.

    Regresa un dict con:
      "total":          número total de préstamos (int)
      "activos":        préstamos sin devolver (int)
      "devueltos":      préstamos devueltos (int)
      "multas_cobradas": suma de "multa" de los préstamos devueltos (float)
      "mas_prestados":  lista de hasta `top` tuplas (titulo, veces_prestado),
                        de la más prestada a la menos; si empatan, por título
                        en orden alfabético (normalizado). Solo libros que se
                        han prestado al menos una vez. Si un libro ya fue
                        eliminado del catálogo, su título es "(eliminado)".
    """
    # TODO: implementar (Actividad 6 · Día 3)
    raise NotImplementedError("Actividad 6 pendiente")
