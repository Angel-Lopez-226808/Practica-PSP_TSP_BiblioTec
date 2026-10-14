"""Configuración de las pruebas y REGISTRO AUTOMÁTICO de resultados.

Cada vez que corren las pruebas, el resultado de cada una se agrega a
registro/ejecuciones.csv. Con ese historial, `python probar.py --reporte`
detecta cuándo una prueba pasó de FALLA a PASA y calcula el tiempo de
corrección de cada defecto. NO MODIFICAR.
"""

import csv
import re
from datetime import date, datetime
from pathlib import Path

import pytest

from nucleo.repositorio import Repositorio
from nucleo.semilla import datos_semilla

# Fecha fija para que las pruebas den siempre el mismo resultado.
HOY = date(2026, 10, 15)

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "registro" / "ejecuciones.csv"
CAMPOS = ["fecha_hora", "ejecucion", "modulo", "actividad", "prueba", "resultado", "mensaje"]
PATRON = re.compile(r"test_(?P<modulo>\w+)\.py::test_f(?P<actividad>\d)_(?P<prueba>[\w\[\]\-. ]+)")
EJECUCION = datetime.now().strftime("%Y%m%d-%H%M%S")


@pytest.fixture
def hoy():
    return HOY


@pytest.fixture
def repo():
    """Repositorio en memoria con los datos de ejemplo (no toca el archivo de la app)."""
    return Repositorio(datos_semilla(HOY))


def _mensaje(report):
    crash = getattr(report.longrepr, "reprcrash", None)
    texto = crash.message if crash else str(report.longrepr)
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    return (lineas[0] if lineas else "")[:180]


def pytest_runtest_logreport(report):
    # Se registra la fase "call" (la prueba en sí) y los errores al preparar datos.
    if report.when != "call" and not (report.when == "setup" and report.failed):
        return
    coincidencia = PATRON.search(report.nodeid)
    if not coincidencia:
        return
    if report.passed:
        resultado, mensaje = "PASA", ""
    else:
        mensaje = _mensaje(report)
        resultado = "PENDIENTE" if "NotImplementedError" in mensaje else "FALLA"
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not REGISTRO.exists()
    with REGISTRO.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if nuevo:
            escritor.writerow(CAMPOS)
        escritor.writerow([
            datetime.now().isoformat(timespec="seconds"), EJECUCION,
            coincidencia["modulo"], coincidencia["actividad"], coincidencia["prueba"],
            resultado, mensaje,
        ])
