"""Datos de ejemplo. Las fechas se calculan a partir de `hoy`
para que siempre haya préstamos vigentes y vencidos. NO MODIFICAR."""

from datetime import date, timedelta


def datos_semilla(hoy=None):
    hoy = hoy or date.today()

    def dia(desplazamiento):
        return (hoy + timedelta(days=desplazamiento)).isoformat()

    libros = [
        (1, "Cien años de soledad", "Gabriel García Márquez", "9780307474728", 1967, "Novela"),
        (2, "Pedro Páramo", "Juan Rulfo", "9786071603579", 1955, "Novela"),
        (3, "Breve historia del tiempo", "Stephen Hawking", "9788498920543", 1988, "Ciencia"),
        (4, "El origen de las especies", "Charles Darwin", "9788420671123", 1859, "Ciencia"),
        (5, "Sapiens", "Yuval Noah Harari", "9786073128355", 2011, "Historia"),
        (6, "Visión de los vencidos", "Miguel León-Portilla", "9786070200795", 1959, "Historia"),
        (7, "Código limpio", "Robert C. Martin", "9788441532106", 2008, "Tecnología"),
        (8, "El programador pragmático", "Andrew Hunt", "9788441545472", 1999, "Tecnología"),
        (9, "Introducción a los algoritmos", "Thomas H. Cormen", "9780262046305", 1990, "Tecnología"),
        (10, "El principito", "Antoine de Saint-Exupéry", "9786070706945", 1943, "Infantil"),
        (11, "Matilda", "Roald Dahl", "9788491221166", 1988, "Infantil"),
        (12, "Como agua para chocolate", "Laura Esquivel", "9786073137258", 1989, "Novela"),
    ]
    prestados = {1, 3, 5, 7, 8, 10}

    socios = [
        (1, "Ana Torres", "ana.torres@correo.com", "6561112233", True, -200),
        (2, "Bruno Díaz", "bruno.diaz@correo.com", "6562223344", True, -180),
        (3, "Carla Méndez", "carla.mendez@correo.com", "6563334455", True, -150),
        (4, "Diego Ramírez", "diego.ramirez@correo.com", "6564445566", True, -120),
        (5, "Elena Ruiz", "elena.ruiz@correo.com", "6565556677", False, -100),
        (6, "Fernando Castillo", "fernando.castillo@correo.com", "6566667788", True, -90),
        (7, "Gabriela Núñez", "gabriela.nunez@correo.com", "6567778899", True, -60),
        (8, "Héctor Salinas", "hector.salinas@correo.com", "6568889900", False, -30),
    ]

    # (id, libro, socio, prestado, límite, devuelto, multa)
    prestamos = [
        (1, 1, 1, -30, -23, -25, 0.0),
        (2, 7, 2, -28, -21, -18, 15.0),
        (3, 1, 3, -20, -13, -14, 0.0),
        (4, 3, 1, -5, 2, None, 0.0),
        (5, 7, 4, -12, -5, None, 0.0),
        (6, 10, 6, -3, 4, None, 0.0),
        (7, 5, 5, -20, -13, None, 0.0),
        (8, 1, 7, -10, -3, -1, 10.0),
        (9, 8, 2, -2, 5, None, 0.0),
        (10, 1, 2, -1, 6, None, 0.0),
    ]

    return {
        "libros": [
            {"id": i, "titulo": t, "autor": a, "isbn": isbn, "anio": anio,
             "categoria": cat, "disponible": i not in prestados}
            for i, t, a, isbn, anio, cat in libros
        ],
        "socios": [
            {"id": i, "nombre": n, "correo": c, "telefono": tel,
             "activo": activo, "fecha_alta": dia(alta)}
            for i, n, c, tel, activo, alta in socios
        ],
        "prestamos": [
            {"id": i, "libro_id": l, "socio_id": s, "fecha_prestamo": dia(p),
             "fecha_limite": dia(lim), "fecha_devolucion": dia(d) if d is not None else None,
             "multa": m}
            for i, l, s, p, lim, d, m in prestamos
        ],
    }
