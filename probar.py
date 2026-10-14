"""Herramienta de la actividad PSP. NO MODIFICAR.

Uso:
  python probar.py libros 2          Corre las pruebas de la actividad 2 del módulo libros
  python probar.py libros            Corre todas las pruebas del módulo libros
  python probar.py --reporte libros  Genera el reporte de defectos detectados en pruebas
  python probar.py --loc libros      Cuenta las LOC de cada función (estándar de la actividad)

Módulos: libros, socios, prestamos
"""

import ast
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
REGISTRO = RAIZ / "registro" / "ejecuciones.csv"
MODULOS = ("libros", "socios", "prestamos")


# ====================================================================== pruebas
def correr_pruebas(modulo, actividad=None):
    import pytest

    argumentos = ["-q", "--tb=line", "-p", "no:cacheprovider", f"pruebas/test_{modulo}.py"]
    if actividad:
        argumentos += ["-k", f"test_f{actividad}_"]
    print(f"\n=== Pruebas de {modulo}" + (f", actividad {actividad}" if actividad else "") + " ===\n")
    filas_antes = len(leer_registro())
    pytest.main(argumentos)
    nuevas = leer_registro()[filas_antes:]
    resumen_ejecucion(modulo, nuevas)


def leer_registro():
    if not REGISTRO.exists():
        return []
    with REGISTRO.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def resumen_ejecucion(modulo, nuevas):
    if not nuevas:
        print("\nNo se ejecutó ninguna prueba. Revisa el nombre del módulo y la actividad.")
        return
    por_actividad = defaultdict(lambda: defaultdict(int))
    for fila in nuevas:
        por_actividad[fila["actividad"]][fila["resultado"]] += 1
    print("\n--- Resumen ---")
    for act in sorted(por_actividad):
        c = por_actividad[act]
        total = sum(c.values())
        if c["PENDIENTE"] == total:
            estado = "PENDIENTE (función sin implementar)"
        elif c["FALLA"] or c["PENDIENTE"]:
            estado = f"{c['PASA']}/{total} pasan"
        else:
            estado = f"{total}/{total} pasan  -> ACTIVIDAD COMPLETA"
        print(f"  Actividad {act}: {estado}")

    ejecucion = nuevas[0]["ejecucion"]
    defectos = detectar_defectos(modulo)
    abiertos = [d for d in defectos if d["ejecucion_inicio"] == ejecucion]
    cerrados = [d for d in defectos if d["ejecucion_fin"] == ejecucion]
    for d in abiertos:
        print(f"\n  [X] Nuevo defecto (act. {d['actividad']}): {d['descripcion']}")
    for d in cerrados:
        print(f"  [OK] Corregido (act. {d['actividad']}) en {d['minutos']} min: {d['descripcion'].split(':')[0]}")
    if abiertos or cerrados:
        print("\n  Quedó registrado automáticamente. Al final del día: python probar.py --reporte " + modulo)


# ====================================================================== defectos
def detectar_defectos(modulo):
    """Recorre el historial y detecta transiciones FALLA -> PASA por prueba.

    Los casos de una misma prueba parametrizada (prueba[caso1], prueba[caso2]...)
    que empiezan a fallar y se corrigen en las mismas ejecuciones se agrupan
    como UN defecto. Si un solo error rompe varias pruebas distintas, aparecen
    varias filas: el alumno las consolida al pasarlas a Excel.
    """
    abiertos = {}      # (actividad, prueba) -> fila de la primera falla
    individuales = []  # defectos por prueba
    for fila in leer_registro():
        if fila["modulo"] != modulo:
            continue
        llave = (fila["actividad"], fila["prueba"])
        if fila["resultado"] == "FALLA" and llave not in abiertos:
            abiertos[llave] = fila
        elif fila["resultado"] == "PASA" and llave in abiertos:
            inicio = abiertos.pop(llave)
            individuales.append((inicio, fila))
    for inicio in abiertos.values():
        individuales.append((inicio, None))

    grupos = {}
    for inicio, fin in individuales:
        prueba_base = inicio["prueba"].split("[")[0]
        llave = (inicio["actividad"], inicio["ejecucion"], fin["ejecucion"] if fin else None, prueba_base)
        grupo = grupos.setdefault(llave, {"inicio": inicio, "fin": fin, "pruebas": [], "mensajes": []})
        grupo["pruebas"].append(inicio["prueba"])
        if inicio["mensaje"] and inicio["mensaje"] not in grupo["mensajes"]:
            grupo["mensajes"].append(inicio["mensaje"])

    # Si varios defectos se corrigen en la misma ejecución, el tiempo entre
    # ejecuciones se reparte en partes iguales entre ellos.
    comparten = defaultdict(int)
    for llave in grupos:
        comparten[(llave[1], llave[2])] += 1

    defectos = []
    for llave, g in sorted(grupos.items(), key=lambda par: (par[1]["inicio"]["fecha_hora"],
                                                             par[1]["inicio"]["actividad"])):
        inicio, fin = g["inicio"], g["fin"]
        minutos = None
        if fin:
            segundos = (datetime.fromisoformat(fin["fecha_hora"])
                        - datetime.fromisoformat(inicio["fecha_hora"])).total_seconds()
            minutos = max(round(segundos / 60 / comparten[(llave[1], llave[2])], 1), 0.1)
        base = g["pruebas"][0].split("[")[0]
        nombre = f"{base} ({len(g['pruebas'])} casos)" if len(g["pruebas"]) > 1 else g["pruebas"][0]
        descripcion = f"{nombre}: {g['mensajes'][0] if g['mensajes'] else ''}".strip()
        defectos.append({
            "actividad": inicio["actividad"],
            "detectado": inicio["fecha_hora"],
            "corregido": fin["fecha_hora"] if fin else "",
            "minutos": minutos,
            "pruebas": g["pruebas"],
            "descripcion": descripcion[:250],
            "ejecucion_inicio": inicio["ejecucion"],
            "ejecucion_fin": fin["ejecucion"] if fin else None,
        })
    return defectos


def reporte(modulo):
    defectos = detectar_defectos(modulo)
    print(f"\n=== Defectos detectados en pruebas — módulo {modulo} ===\n")
    if not defectos:
        print("Todavía no hay defectos registrados en pruebas para este módulo.")
        return
    for i, d in enumerate(defectos, 1):
        corregido = d["corregido"][11:16] if d["corregido"] else "SIN CORREGIR"
        minutos = f"{d['minutos']} min" if d["minutos"] is not None else "-"
        print(f"{i:>2}. Act {d['actividad']} | {d['detectado'][11:16]} -> {corregido} | {minutos:>8} | {d['descripcion']}")

    hoy = datetime.now().date().isoformat()
    de_hoy = [d for d in defectos if d["detectado"].startswith(hoy)]
    salida = RAIZ / "registro" / f"reporte_defectos_{modulo}.txt"
    with salida.open("w", encoding="utf-8", newline="") as archivo:
        for d in de_hoy:
            minutos = "" if d["minutos"] is None else str(d["minutos"])
            texto = d["descripcion"].replace("\t", " ")
            # Columnas: Actividad | Fase de remoción | Min corrección | Tipo | Fase de inyección | Descripción
            archivo.write(f"{d['actividad']}\tPruebas\t{minutos}\t\t\t{texto}\r\n")
    print(f"\nArchivo para Excel: {salida.relative_to(RAIZ)}  ({len(de_hoy)} defectos detectados HOY)")
    print("Solo incluye los defectos de hoy, para que no pegues dos veces los de días anteriores.")
    print("Ábrelo, selecciona todo (Ctrl+A), copia y pega en la primera celda libre de la")
    print("columna 'Act.' de tu registro de defectos en Excel.")
    print("Luego completa a mano las columnas 'Tipo' y 'Fase de inyección'.")
    print("Si varias filas son la MISMA causa, déjalas en una sola y suma sus minutos.")
    if any(d["minutos"] is None for d in defectos):
        print("\nOJO: hay defectos SIN CORREGIR; vuelve a correr las pruebas cuando los arregles.")


# ====================================================================== LOC
def contar_loc(modulo):
    ruta = RAIZ / "modulos" / f"{modulo}.py"
    codigo = ruta.read_text(encoding="utf-8")
    lineas = codigo.splitlines()
    arbol = ast.parse(codigo)
    print(f"\n=== LOC por función — modulos/{modulo}.py ===")
    print("Estándar: líneas del CUERPO de la función, sin docstring, sin líneas en blanco")
    print("y sin comentarios. La línea del 'def' no cuenta.\n")
    total = 0
    for nodo in arbol.body:
        if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        cuerpo = nodo.body
        doc = ast.get_docstring(nodo)
        if doc is not None:
            cuerpo = cuerpo[1:]
        if not cuerpo:
            continue
        pendiente = (len(cuerpo) == 1 and isinstance(cuerpo[0], ast.Raise)
                     and "NotImplementedError" in ast.unparse(cuerpo[0]))
        rango = lineas[cuerpo[0].lineno - 1: nodo.end_lineno]
        loc = sum(1 for l in rango if l.strip() and not l.strip().startswith("#"))
        actividad = ""
        if doc and doc.startswith("Actividad"):
            actividad = doc.split("—")[0].strip()
        elif nodo.name.startswith("_"):
            actividad = "auxiliar: suma sus LOC a la actividad donde la creaste"
        if pendiente:
            print(f"  {nodo.name:<28} PENDIENTE   ({actividad})")
        else:
            total += loc
            print(f"  {nodo.name:<28} {loc:>4} LOC   ({actividad})")
    print(f"\n  Total implementado: {total} LOC")


# ====================================================================== entrada
def main(argv):
    if len(argv) < 1 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] in ("--reporte", "--loc"):
        if len(argv) < 2 or argv[1] not in MODULOS:
            print(f"Indica el módulo: {', '.join(MODULOS)}")
            return
        (reporte if argv[0] == "--reporte" else contar_loc)(argv[1])
        return
    modulo = argv[0]
    if modulo not in MODULOS:
        print(f"Módulo desconocido '{modulo}'. Usa: {', '.join(MODULOS)}")
        return
    actividad = argv[1] if len(argv) > 1 else None
    if actividad and actividad not in ("1", "2", "3", "4", "5", "6"):
        print("La actividad debe ser un número del 1 al 6")
        return
    correr_pruebas(modulo, actividad)


if __name__ == "__main__":
    main(sys.argv[1:])
