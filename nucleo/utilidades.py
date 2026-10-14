"""Funciones de apoyo que pueden usar los tres módulos. NO MODIFICAR."""

import unicodedata
from datetime import date


def normalizar(texto):
    """Convierte a minúsculas, quita acentos y espacios de los extremos.

    normalizar("  Pedro PÁRAMO ") -> "pedro paramo"
    """
    if texto is None:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    sin_acentos = "".join(c for c in texto if not unicodedata.combining(c))
    return sin_acentos.strip().lower()


def solo_digitos(texto):
    """Quita espacios y guiones. solo_digitos("656-111 2233") -> "6561112233" """
    return str(texto).replace("-", "").replace(" ", "")


def a_fecha(valor):
    """Acepta un objeto date o un texto "AAAA-MM-DD" y regresa un date."""
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(str(valor))


def hoy_o(hoy=None):
    """Regresa la fecha recibida o, si es None, la fecha de hoy.

    Las funciones que dependen de la fecha reciben un parámetro `hoy`
    para que las pruebas puedan usar siempre la misma fecha.
    """
    return a_fecha(hoy) if hoy is not None else date.today()
