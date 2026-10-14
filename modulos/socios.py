"""MÓDULO SOCIOS — Integrante B.

Cada función tiene su especificación en el docstring. Implementa solo
el cuerpo; no cambies el nombre ni los parámetros, porque la app y las
pruebas dependen de ellos.

Datos de un socio:
    {"id": 1, "nombre": "Ana Torres", "correo": "ana.torres@correo.com",
     "telefono": "6561112233", "activo": True, "fecha_alta": "2026-03-26"}

Un préstamo está ACTIVO si su fecha_devolucion es None, y VENCIDO si
además su fecha_limite es anterior a `hoy`.
Para errores de validación lanza ValueError("mensaje claro").
"""

from nucleo.config import CAMPOS_EDITABLES_SOCIO, LONGITUD_TELEFONO
from nucleo.utilidades import a_fecha, hoy_o, normalizar, solo_digitos


def listar_socios(repo, solo_activos=False):
    """Actividad 1 · Día 1 — Listar socios.

    Regresa los socios ordenados por nombre (normalizado, sin acentos).
    Si solo_activos es True, regresa únicamente los que tienen activo True.
    A cada socio le agrega la llave "estado": "Activo" o "Suspendido".
    """
    # TODO: implementar (Actividad 1 · Día 1)
    raise NotImplementedError("Actividad 1 pendiente")


def registrar_socio(repo, nombre, correo, telefono, hoy=None):
    """Actividad 2 · Día 1 — Registrar socio con validación.

    Reglas (si alguna falla, lanza ValueError):
      - nombre no puede quedar vacío (después de quitar espacios).
      - correo: se guarda sin espacios y en minúsculas. Debe tener
        exactamente un "@", texto antes del "@", y después del "@" un
        dominio que contenga al menos un "." que no esté ni al inicio
        ni al final del dominio. ("a@b.com" es válido; "a@.com", "a@com",
        "a@b.", "@b.com" y "a@@b.com" no lo son).
      - No puede existir otro socio con el mismo correo.
      - telefono: se le quitan guiones y espacios (solo_digitos); debe quedar
        con exactamente 10 dígitos numéricos.
    Guarda: nombre sin espacios extra, correo limpio, telefono limpio,
    "activo": True y "fecha_alta": hoy en formato "AAAA-MM-DD"
    (usa hoy_o(hoy).isoformat()).
    Regresa el id asignado.
    """
    # TODO: implementar (Actividad 2 · Día 1)
    raise NotImplementedError("Actividad 2 pendiente")


def buscar_socios(repo, texto):
    """Actividad 3 · Día 2 — Buscar socio por nombre o número.

      - Si texto (sin espacios extra) son solo dígitos, se interpreta como
        número de socio: regresa [socio] si existe ese id, o [] si no.
      - Si no, regresa los socios cuyo nombre contenga el texto, sin importar
        mayúsculas ni acentos ("nunez" encuentra "Gabriela Núñez").
      - Si texto está vacío, regresa todos.
    El resultado va ordenado por nombre y con la llave "estado", igual que
    listar_socios.
    """
    # TODO: implementar (Actividad 3 · Día 2)
    raise NotImplementedError("Actividad 3 pendiente")


def editar_socio(repo, socio_id, cambios):
    """Actividad 4 · Día 2 — Editar socio.

    `cambios` es un dict, por ejemplo {"telefono": "656 000 1111"}.
      - Si el socio no existe -> ValueError.
      - Solo se pueden cambiar los campos de CAMPOS_EDITABLES_SOCIO
        (nombre, correo, telefono). Cualquier otro -> ValueError.
      - Se validan y limpian con las mismas reglas de registrar_socio.
        El correo no puede repetirse con el de OTRO socio (sí puede
        "cambiarse" por el mismo que ya tiene).
    Regresa el socio actualizado (el dict que regresa repo.actualizar).
    """
    # TODO: implementar (Actividad 4 · Día 2)
    raise NotImplementedError("Actividad 4 pendiente")


def cambiar_estado_socio(repo, socio_id, activo, hoy=None):
    """Actividad 5 · Día 3 — Suspender o reactivar socio.

      - Si el socio no existe -> ValueError.
      - activo=False: suspende al socio (siempre se permite).
      - activo=True: reactiva al socio, PERO si tiene algún préstamo vencido
        (activo y con fecha_limite anterior a `hoy`) -> ValueError.
    Regresa el socio actualizado.
    """
    # TODO: implementar (Actividad 5 · Día 3)
    raise NotImplementedError("Actividad 5 pendiente")


def estadisticas_socios(repo, hoy=None):
    """Actividad 6 · Día 3 — Estadísticas de socios.

    Regresa un dict con estas llaves (todas enteras):
      "total":         número de socios
      "activos":       socios con activo True
      "suspendidos":   socios con activo False
      "con_prestamos": socios DISTINTOS con al menos un préstamo activo
      "con_vencidos":  socios DISTINTOS con al menos un préstamo vencido
    """
    # TODO: implementar (Actividad 6 · Día 3)
    raise NotImplementedError("Actividad 6 pendiente")
