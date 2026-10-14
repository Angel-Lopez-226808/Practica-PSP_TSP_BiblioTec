# BiblioTec · Actividad PSP/TSP

BiblioTec es una mini biblioteca web en Python (Flask). La app, el diseño y
las pruebas **ya están hechos**. Tu trabajo es programar las **6 funciones de
tu módulo** y **medir tu propio proceso** con PSP mientras lo haces.

| Integrante | Módulo | Archivo |
|---|---|---|
| A | Libros | `modulos/libros.py` |
| B | Socios | `modulos/socios.py` |
| C | Préstamos | `modulos/prestamos.py` |

## 1. Instalación (antes del día 1)

Necesitas Python 3.10 o superior.

```bash
pip install flask pytest
python app.py
```

Abre http://127.0.0.1:5000 en tu navegador. Las secciones que aún no programas
aparecen como **Pendiente**: es normal.

Cada integrante trabaja en **su propia copia** de la carpeta `bibliotec`.

## 2. Reglas

- Solo modificas **tu archivo** dentro de `modulos/`.
- **No** modifiques `app.py`, `nucleo/`, `pruebas/`, `templates/` ni `static/`.
- No cambies el nombre ni los parámetros de las funciones.
- Puedes crear funciones auxiliares (que empiecen con `_`) dentro de tu archivo.
- Lee la especificación completa en el docstring de cada función **antes** de programar.

## 3. Las 6 actividades

| Día | Nivel PSP | Actividades | Qué cambia en tu proceso |
|---|---|---|---|
| 1 | PSP0 · medir | 1 y 2 | Registras tiempo, LOC y defectos. Estimas "a ojo". |
| 2 | PSP1 · estimar | 3 y 4 | Estimas con tu productividad del día 1 (columna *Min sugeridos* del Excel). |
| 3 | PSP2 · revisar | 5 y 6 | Antes de correr las pruebas, revisas tu código con tu checklist (`CHECKLIST_REVISION.md`). |

Cada actividad debe tomar unos **15 minutos**.

## 4. Ciclo de cada actividad

1. **Planeación (1–2 min).** Lee la especificación. Anota en tu hoja de Excel las
   *LOC estimadas* y los *Min estimados*. Arranca tu cronómetro.
2. **Código.** Programa la función. Si encuentras y corriges un error mientras
   programas (por ejemplo, un error de sintaxis al guardar), anótalo en el
   registro de defectos con *Fase de remoción = Código*.
3. **Revisión (solo día 3, 2–3 min).** Recorre tu checklist línea por línea. Cada
   error que encuentres se anota con *Fase de remoción = Revisión*.
4. **Pruebas.** Corre las pruebas de la actividad:

   ```bash
   python probar.py libros 2      # módulo libros, actividad 2
   ```

   Si alguna falla, corrige y vuelve a correr hasta que diga
   `ACTIVIDAD COMPLETA`. **Los defectos encontrados en pruebas se registran
   solos**, con su hora de detección y su tiempo de corrección.
5. **Cierre.** Cuenta tus LOC y anota en Excel los minutos de cada fase y las
   *LOC reales*:

   ```bash
   python probar.py --loc libros
   ```

## 5. Al final de cada día (postmortem, 5–10 min)

```bash
python probar.py --reporte libros
```

Esto genera `registro/reporte_defectos_libros.txt`. Ábrelo, selecciona todo,
copia y pégalo en la **primera celda libre de la columna "Act."** del registro de
defectos de tu hoja. Después completa a mano:

- **Tipo** de defecto (lista desplegable).
- **Fase de inyección**: dónde cometiste el error (casi siempre *Código*;
  *Planeación* si entendiste mal la especificación).

Si varias filas del reporte son **la misma causa**, déjalas en una sola fila
y suma sus minutos. Si un solo error tiene varias causas, sepáralo.

En pantalla verás todo el historial, pero el archivo solo trae los defectos
**detectados hoy**, para que no pegues dos veces los de días anteriores.

## 6. Estándar de conteo de LOC

Para que todos midan igual:

- Se cuentan las líneas del **cuerpo** de la función.
- **No** se cuentan: la línea del `def`, el docstring, líneas en blanco ni comentarios.
- Una instrucción partida en varias líneas cuenta cada línea.
- Las funciones auxiliares (`_algo`) se suman a la actividad en la que las creaste.

`python probar.py --loc <modulo>` aplica este estándar automáticamente.

## 7. Tipos de defecto (estándar PSP)

| Tipo | Ejemplos |
|---|---|
| 10 Documentación | Comentarios o mensajes incorrectos |
| 20 Sintaxis | Faltan `:`, paréntesis, indentación, nombre mal escrito |
| 30 Build/paquetes | `import` faltante o incorrecto |
| 40 Asignación | Variable mal inicializada o con el alcance equivocado |
| 50 Interfaz | Llave o parámetro equivocado: `p["libro"]` en vez de `p["libro_id"]` |
| 60 Validación | Faltó validar una regla de la especificación |
| 70 Datos | Tipo de dato incorrecto: texto vs número, `str` vs `date` |
| 80 Función | Lógica incorrecta: condición, ciclo, cálculo, orden |
| 90 Sistema | Configuración, tiempos, memoria |
| 100 Entorno | Problemas con el editor, Python o herramientas |

## 8. Integración del equipo (final del día 3)

1. En una sola copia del proyecto, reemplaza los tres archivos de `modulos/`
   por los de cada integrante.
2. Corre todas las pruebas: `python -m pytest`
3. Abre la app y revisen juntos que las tres secciones y el **Inicio** funcionan.
4. Cualquier problema que aparezca aquí se registra como defecto de tipo
   *50 Interfaz* en la hoja del integrante responsable.

## 9. Comandos

| Comando | Para qué |
|---|---|
| `python app.py` | Levanta la app en http://127.0.0.1:5000 |
| `python app.py --reiniciar` | Restaura los datos de ejemplo |
| `python probar.py libros 3` | Pruebas de la actividad 3 de libros |
| `python probar.py libros` | Todas las pruebas de libros |
| `python probar.py --reporte libros` | Reporte de defectos para Excel |
| `python probar.py --loc libros` | LOC por función |

## 10. Datos útiles para programar

```python
repo.listar("libros")                      # lista de dicts (copias)
repo.obtener("socios", 3)                  # dict o None
repo.agregar("prestamos", {...})           # regresa el id nuevo
repo.actualizar("libros", 3, {"anio": 1990})
repo.eliminar("libros", 3)                 # True / False
repo.filtrar("prestamos", lambda p: p["socio_id"] == 2)
```

Funciones de apoyo en `nucleo/utilidades.py`: `normalizar()`, `solo_digitos()`,
`a_fecha()`, `hoy_o()`. Reglas de negocio en `nucleo/config.py`.

Las fechas se guardan como texto `"AAAA-MM-DD"`. Para compararlas o restarlas,
conviértelas con `a_fecha()`.
