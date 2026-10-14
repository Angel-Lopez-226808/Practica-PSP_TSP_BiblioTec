"""Pruebas del módulo PRÉSTAMOS. NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

from datetime import date, timedelta

import pytest

from modulos.prestamos import (
    calcular_multa, listar_prestamos_activos, prestamos_vencidos, registrar_devolucion,
    registrar_prestamo, reporte_prestamos,
)


def ids(prestamos):
    return [p["id"] for p in prestamos]


# ------------------------------------------------------------ Actividad 1
def test_f1_solo_activos_ordenados_por_limite(repo):
    assert ids(listar_prestamos_activos(repo)) == [7, 5, 4, 6, 9, 10], \
        "Deben ir los 6 préstamos activos, del límite más próximo al más lejano"


def test_f1_agrega_titulo_y_socio(repo):
    primero = listar_prestamos_activos(repo)[0]
    assert primero["titulo"] == "Sapiens", "La llave 'titulo' debe tener el título del libro"
    assert primero["socio"] == "Elena Ruiz", "La llave 'socio' debe tener el nombre del socio"


def test_f1_empate_por_id(repo):
    repo.actualizar("prestamos", 6, {"fecha_limite": "2026-10-17"})  # igual que el préstamo 4
    assert ids(listar_prestamos_activos(repo))[2:4] == [4, 6], "Si empatan en fecha límite, se ordenan por id"


# ------------------------------------------------------------ Actividad 2
def test_f2_registra_prestamo(repo, hoy):
    nuevo_id = registrar_prestamo(repo, 2, 3, hoy)
    assert nuevo_id == 11
    p = repo.obtener("prestamos", nuevo_id)
    assert p["fecha_prestamo"] == "2026-10-15", "fecha_prestamo debe ser hoy (AAAA-MM-DD)"
    assert p["fecha_limite"] == "2026-10-22", "fecha_limite debe ser hoy + 7 días"
    assert p["fecha_devolucion"] is None and p["multa"] == 0.0


def test_f2_marca_libro_no_disponible(repo, hoy):
    registrar_prestamo(repo, 2, 3, hoy)
    assert repo.obtener("libros", 2)["disponible"] is False, "El libro prestado debe quedar no disponible"


@pytest.mark.parametrize("libro_id, socio_id", [
    (1, 3),    # libro ya prestado
    (99, 3),   # libro inexistente
    (2, 5),    # socio suspendido
    (2, 99),   # socio inexistente
])
def test_f2_valida_libro_y_socio(repo, hoy, libro_id, socio_id):
    with pytest.raises(ValueError):
        registrar_prestamo(repo, libro_id, socio_id, hoy)
    assert len(repo.listar("prestamos")) == 10, "Si hay error no se debe crear el préstamo"


def test_f2_maximo_de_prestamos(repo, hoy):
    registrar_prestamo(repo, 2, 2, hoy)  # Bruno llega a 3 préstamos activos
    with pytest.raises(ValueError):
        registrar_prestamo(repo, 4, 2, hoy)
    assert repo.obtener("libros", 4)["disponible"] is True, "Si se rechaza, el libro sigue disponible"


# ------------------------------------------------------------ Actividad 3
def test_f3_multa_por_dias_de_retraso():
    assert calcular_multa("2026-10-10", "2026-10-13") == 15.0


def test_f3_sin_retraso_no_hay_multa():
    assert calcular_multa("2026-10-10", "2026-10-10") == 0.0, "Devolver el mismo día no genera multa"
    assert calcular_multa("2026-10-10", "2026-10-02") == 0.0, "Devolver antes no genera multa negativa"


def test_f3_acepta_objetos_date():
    assert calcular_multa(date(2026, 9, 28), date(2026, 10, 3)) == 25.0, "Debe funcionar entre meses"


def test_f3_regresa_float():
    assert isinstance(calcular_multa("2026-10-10", "2026-10-11"), float)


# ------------------------------------------------------------ Actividad 4
def test_f4_devolucion_con_retraso(repo, hoy):
    assert registrar_devolucion(repo, 5, hoy) == 25.0, "El préstamo 5 venció hace 5 días: $25"
    p = repo.obtener("prestamos", 5)
    assert p["fecha_devolucion"] == "2026-10-15" and p["multa"] == 25.0, "Debe guardar fecha y multa"


def test_f4_devolucion_a_tiempo(repo, hoy):
    assert registrar_devolucion(repo, 4, hoy) == 0.0


def test_f4_libro_vuelve_a_estar_disponible(repo, hoy):
    registrar_devolucion(repo, 5, hoy)
    assert repo.obtener("libros", 7)["disponible"] is True


@pytest.mark.parametrize("prestamo_id", [1, 99])
def test_f4_ya_devuelto_o_inexistente(repo, hoy, prestamo_id):
    with pytest.raises(ValueError):
        registrar_devolucion(repo, prestamo_id, hoy)


# ------------------------------------------------------------ Actividad 5
def test_f5_lista_vencidos_ordenados(repo, hoy):
    vencidos = prestamos_vencidos(repo, hoy)
    assert ids(vencidos) == [7, 5], "Vencidos de mayor a menor retraso"
    assert [p["dias_retraso"] for p in vencidos] == [13, 5]
    assert [p["multa_estimada"] for p in vencidos] == [65.0, 25.0]


def test_f5_incluye_titulo_y_socio(repo, hoy):
    p = prestamos_vencidos(repo, hoy)[1]
    assert p["titulo"] == "Código limpio" and p["socio"] == "Diego Ramírez"


def test_f5_depende_de_la_fecha(repo, hoy):
    assert ids(prestamos_vencidos(repo, hoy + timedelta(days=3))) == [7, 5, 4], \
        "Tres días después, el préstamo 4 también está vencido"


def test_f5_ignora_devueltos(repo, hoy):
    repo.actualizar("prestamos", 7, {"fecha_devolucion": "2026-10-15"})
    assert ids(prestamos_vencidos(repo, hoy)) == [5], "Un préstamo devuelto ya no está vencido"


# ------------------------------------------------------------ Actividad 6
def test_f6_totales(repo):
    r = reporte_prestamos(repo)
    assert (r["total"], r["activos"], r["devueltos"]) == (10, 6, 4)
    assert r["multas_cobradas"] == 25.0 and isinstance(r["multas_cobradas"], float)


def test_f6_mas_prestados(repo):
    assert reporte_prestamos(repo)["mas_prestados"] == [
        ("Cien años de soledad", 4), ("Código limpio", 2), ("Breve historia del tiempo", 1),
    ], "Top 3 por veces prestado; los empates van por título"


def test_f6_parametro_top(repo):
    assert reporte_prestamos(repo, top=1)["mas_prestados"] == [("Cien años de soledad", 4)]


def test_f6_libro_eliminado(repo):
    repo.eliminar("libros", 1)
    assert reporte_prestamos(repo)["mas_prestados"][0] == ("(eliminado)", 4)
