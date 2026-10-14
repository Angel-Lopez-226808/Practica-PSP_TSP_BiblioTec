"""Reglas de negocio compartidas por los tres módulos. NO MODIFICAR."""

# Libros
CATEGORIAS = ["Novela", "Ciencia", "Historia", "Tecnología", "Infantil"]
ANIO_MINIMO = 1450          # año de la imprenta de Gutenberg
LONGITUD_ISBN = 13
CAMPOS_EDITABLES_LIBRO = ["titulo", "autor", "anio", "categoria"]
ORDENES_LIBRO = ["titulo", "autor", "anio"]

# Socios
LONGITUD_TELEFONO = 10
CAMPOS_EDITABLES_SOCIO = ["nombre", "correo", "telefono"]

# Préstamos
DIAS_PRESTAMO = 7           # días que dura un préstamo
MULTA_POR_DIA = 5.0         # pesos por cada día de retraso
MAX_PRESTAMOS_ACTIVOS = 3   # préstamos simultáneos permitidos por socio
