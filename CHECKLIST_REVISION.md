# Checklist de revisión de código (Día 3)

Úsalo en las actividades 5 y 6, **antes** de correr las pruebas.
Revisa tu función completa contra cada punto. Cada error que encuentres se
anota en Excel con *Fase de remoción = Revisión*.

## Mis defectos más frecuentes (días 1 y 2)

Antes de empezar el día 3, mira la sección **D. Análisis de defectos** de tu
hoja de Excel y escribe aquí los 3 tipos que más se repitieron, con algo
concreto que debes buscar:

| # | Tipo | Qué voy a buscar |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

## Puntos generales

- [ ] Leí otra vez la especificación (docstring) y cada regla tiene su código.
- [ ] Cada caso inválido de la especificación lanza `ValueError`.
- [ ] Reviso que el registro exista (`obtener()` puede regresar `None`).
- [ ] Uso las llaves correctas de los diccionarios (`libro_id`, `socio_id`, `fecha_limite`...).
- [ ] Convierto tipos cuando hace falta: texto a `int`, texto a fecha con `a_fecha()`.
- [ ] Guardo las fechas como texto `"AAAA-MM-DD"` (`.isoformat()`).
- [ ] Las comparaciones de texto ignoran mayúsculas y acentos cuando la especificación lo pide (`normalizar()`).
- [ ] El orden del resultado es el que pide la especificación, incluido el desempate.
- [ ] Si hay error, no guardo nada a medias (valido primero, guardo después).
- [ ] Regreso exactamente lo que pide la especificación (tipo y forma).
- [ ] No hay errores de sintaxis ni de indentación.
- [ ] Los `import` que uso están al inicio del archivo.
