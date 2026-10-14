"""Pruebas del módulo SOCIOS. NO MODIFICAR.
El nombre test_fN_... indica la actividad (N) que se está probando."""

from datetime import timedelta

import pytest

from modulos.socios import (
    buscar_socios, cambiar_estado_socio, editar_socio, estadisticas_socios, listar_socios, registrar_socio,
)


def ids(socios):
    return [s["id"] for s in socios]


# ------------------------------------------------------------ Actividad 1
def test_f1_regresa_todos_ordenados(repo):
    assert ids(listar_socios(repo)) == [1, 2, 3, 4, 5, 6, 7, 8], "Deben ir los 8 socios ordenados por nombre"


def test_f1_orden_sin_acentos(repo):
    repo.agregar("socios", {"nombre": "Álvaro Peña", "correo": "a@p.com", "telefono": "6560000000",
                            "activo": True, "fecha_alta": "2026-10-01"})
    assert listar_socios(repo)[0]["nombre"] == "Álvaro Peña", "'Álvaro' va antes de 'Ana' (orden sin acentos)"


def test_f1_solo_activos(repo):
    activos = listar_socios(repo, solo_activos=True)
    assert len(activos) == 6, "Hay 6 socios activos"
    assert all(s["activo"] for s in activos)


def test_f1_agrega_llave_estado(repo):
    por_id = {s["id"]: s for s in listar_socios(repo)}
    assert por_id[1]["estado"] == "Activo"
    assert por_id[5]["estado"] == "Suspendido"


# ------------------------------------------------------------ Actividad 2
def test_f2_registra_y_regresa_id(repo, hoy):
    nuevo_id = registrar_socio(repo, "Luis Mora", "luis.mora@correo.com", "6561234567", hoy)
    assert nuevo_id == 9
    socio = repo.obtener("socios", nuevo_id)
    assert socio is not None, "El socio no se guardó"
    assert socio["activo"] is True, "Un socio nuevo debe quedar activo"
    assert socio["fecha_alta"] == "2026-10-15", "fecha_alta debe ser hoy en formato AAAA-MM-DD"


def test_f2_limpia_datos(repo, hoy):
    nuevo_id = registrar_socio(repo, "  Luis Mora ", "  Luis.Mora@Correo.COM ", "656-123 4567", hoy)
    socio = repo.obtener("socios", nuevo_id)
    assert socio["nombre"] == "Luis Mora", "Nombre sin espacios extra"
    assert socio["correo"] == "luis.mora@correo.com", "Correo sin espacios y en minúsculas"
    assert socio["telefono"] == "6561234567", "Teléfono sin guiones ni espacios"


@pytest.mark.parametrize("correo", ["luis.correo.com", "@correo.com", "luis@correo", "luis@.com",
                                    "luis@correo.", "luis@@correo.com", "luis@a@b.com"])
def test_f2_correo_invalido(repo, hoy, correo):
    with pytest.raises(ValueError):
        registrar_socio(repo, "Luis Mora", correo, "6561234567", hoy)


def test_f2_correo_duplicado_sin_importar_mayusculas(repo, hoy):
    with pytest.raises(ValueError):
        registrar_socio(repo, "Otra Ana", "ANA.TORRES@correo.com", "6561234567", hoy)


@pytest.mark.parametrize("telefono", ["12345", "65612345678", "656abc4567", ""])
def test_f2_telefono_invalido(repo, hoy, telefono):
    with pytest.raises(ValueError):
        registrar_socio(repo, "Luis Mora", "luis.mora@correo.com", telefono, hoy)


def test_f2_nombre_vacio(repo, hoy):
    with pytest.raises(ValueError):
        registrar_socio(repo, "   ", "luis.mora@correo.com", "6561234567", hoy)


# ------------------------------------------------------------ Actividad 3
def test_f3_busca_por_nombre_sin_acentos(repo):
    assert ids(buscar_socios(repo, "nunez")) == [7], "'nunez' debe encontrar a Gabriela Núñez"
    assert ids(buscar_socios(repo, "DÍAZ")) == [2], "Sin importar mayúsculas ni acentos"


def test_f3_busca_por_numero(repo):
    assert ids(buscar_socios(repo, "3")) == [3], "Un texto numérico se busca como número de socio"
    assert ids(buscar_socios(repo, " 4 ")) == [4], "Se ignoran los espacios alrededor del número"
    assert buscar_socios(repo, "99") == [], "Número inexistente regresa lista vacía"


def test_f3_texto_vacio_regresa_todos(repo):
    assert len(buscar_socios(repo, "")) == 8


def test_f3_ordenado_y_con_estado(repo):
    resultado = buscar_socios(repo, "r")
    assert ids(resultado) == sorted(ids(resultado)), "Debe ir ordenado por nombre"
    assert all("estado" in s for s in resultado)


# ------------------------------------------------------------ Actividad 4
def test_f4_edita_y_limpia(repo):
    socio = editar_socio(repo, 3, {"telefono": "656 000-1111", "nombre": " Carla M. "})
    assert socio["telefono"] == "6560001111"
    assert socio["nombre"] == "Carla M."
    assert repo.obtener("socios", 3)["telefono"] == "6560001111", "El cambio debe quedar guardado"


def test_f4_puede_conservar_su_propio_correo(repo):
    socio = editar_socio(repo, 1, {"correo": "ANA.TORRES@correo.com"})
    assert socio["correo"] == "ana.torres@correo.com"


def test_f4_correo_de_otro_socio(repo):
    with pytest.raises(ValueError):
        editar_socio(repo, 1, {"correo": "bruno.diaz@correo.com"})


@pytest.mark.parametrize("cambios", [{"activo": False}, {"fecha_alta": "2020-01-01"}])
def test_f4_campo_no_editable(repo, cambios):
    with pytest.raises(ValueError):
        editar_socio(repo, 1, cambios)


@pytest.mark.parametrize("cambios", [{"telefono": "123"}, {"correo": "malo"}, {"nombre": ""}])
def test_f4_valida_valores(repo, cambios):
    with pytest.raises(ValueError):
        editar_socio(repo, 1, cambios)
    assert repo.obtener("socios", 1)["telefono"] == "6561112233", "Si hay error no debe guardar nada"


def test_f4_socio_inexistente(repo):
    with pytest.raises(ValueError):
        editar_socio(repo, 99, {"nombre": "X"})


# ------------------------------------------------------------ Actividad 5
def test_f5_suspende(repo, hoy):
    socio = cambiar_estado_socio(repo, 4, False, hoy)
    assert socio["activo"] is False
    assert repo.obtener("socios", 4)["activo"] is False


def test_f5_reactiva_sin_vencidos(repo, hoy):
    assert cambiar_estado_socio(repo, 8, True, hoy)["activo"] is True, "Héctor no tiene préstamos: puede reactivarse"


def test_f5_reactiva_con_prestamo_vigente(repo, hoy):
    cambiar_estado_socio(repo, 1, False, hoy)
    assert cambiar_estado_socio(repo, 1, True, hoy)["activo"] is True, "Un préstamo NO vencido no impide reactivar"


def test_f5_no_reactiva_con_vencidos(repo, hoy):
    with pytest.raises(ValueError):
        cambiar_estado_socio(repo, 5, True, hoy)
    assert repo.obtener("socios", 5)["activo"] is False


def test_f5_socio_inexistente(repo, hoy):
    with pytest.raises(ValueError):
        cambiar_estado_socio(repo, 99, False, hoy)


# ------------------------------------------------------------ Actividad 6
def test_f6_estadisticas(repo, hoy):
    assert estadisticas_socios(repo, hoy) == {
        "total": 8, "activos": 6, "suspendidos": 2, "con_prestamos": 5, "con_vencidos": 2,
    }


def test_f6_cuenta_socios_distintos(repo, hoy):
    # Bruno (socio 2) tiene dos préstamos activos: se cuenta una sola vez.
    repo.actualizar("prestamos", 4, {"fecha_devolucion": "2026-10-15"})
    assert estadisticas_socios(repo, hoy)["con_prestamos"] == 4


def test_f6_depende_de_la_fecha(repo, hoy):
    assert estadisticas_socios(repo, hoy + timedelta(days=3))["con_vencidos"] == 3, \
        "Tres días después, el préstamo de Ana también está vencido"
