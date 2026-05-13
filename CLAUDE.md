# BI Developer MCP — Reglas de Comportamiento Obligatorias

Este archivo define el comportamiento estricto que Claude debe seguir en CADA sesión de trabajo con dashboards y visualización de datos.

---

## SCOPE DEL PROYECTO

DataPocket MCP es un agente de BI universal. A partir de cualquier fuente de datos (CSV, JSON, Excel, SQL), genera el paquete completo de conexión y analítica para las viz tools más usadas del mercado, organizadas por ecosistema:

| Ecosistema | Tool | Tool MCP | Estado |
|---|---|---|---|
| Microsoft | Power BI Desktop | `datapocket_powerbi_setup` | ✅ Activo |
| Salesforce | Tableau Desktop / Public | `datapocket_tableau_setup` | ✅ Activo |
| Google | Looker / Looker Studio | `datapocket_looker_setup` | ✅ Activo |
| Amazon | QuickSight | `datapocket_quicksight_setup` | ✅ Activo |

**"Paquete completo"** significa, para cada tool:
- Código de **conexión** a la fuente de datos (M, .tds XML, LookML connection, manifest JSON)
- Código de **transformación/semántica** (DAX, LOD expressions, LookML views, QuickSight calculated fields)
- **Instrucciones paso a paso** para el usuario sin conocimiento técnico avanzado
- **Nota de costos** comparativa con las alternativas

---

## FLUJO DE TRABAJO: DOS FASES OBLIGATORIAS

### FASE 1 — LEER Y CONFIRMAR LA DATA (SIEMPRE PRIMERO)

Antes de tocar cualquier archivo HTML, CSS, JS o generar código de viz tool:

1. **Leer el archivo de datos** indicado por el usuario (CSV, JSON, Excel, etc.)
2. **Responder con un resumen estructurado** que incluya:
   - Nombre del archivo leído
   - Tipo de datos que contiene
   - Lista de campos / columnas encontrados
   - Cantidad de registros
   - Rango de fechas (si aplica)
   - 3–5 métricas o insights clave encontrados en los datos
   - Confirmación explícita: _"Solo usaré estos datos. No agregaré información externa."_
3. **Esperar confirmación del usuario** ("ok", "procede", "sí", etc.) antes de continuar.

> **PROHIBIDO** avanzar a la Fase 2 sin confirmación explícita del usuario.

---

### FASE 2 — GENERAR EL OUTPUT (SOLO TRAS CONFIRMACIÓN)

#### REGLAS DE DATOS (irrompibles)

- Usar **ÚNICAMENTE** los datos del archivo proporcionado. Cero inventos.
- Si un campo no existe en el archivo, **no mostrarlo**.
- Todos los números, etiquetas y categorías deben coincidir **exactamente** con el archivo.
- Si los datos son insuficientes para un tipo de gráfico o cálculo, usar una alternativa más simple.
- **Nunca** rellenar datos faltantes con suposiciones o promedios inventados.

#### DISEÑO DE DASHBOARDS HTML — KanbanPro Style

Aplica cuando se genera el dashboard mobile-first (`datapocket_generate_dashboard`):

- Fondo oscuro `#1e1e2f`, texto blanco, acentos neón verde `#39ff8e` y azul `#5bc8fc`
- Mobile-first: `viewport` meta tag, layout Flexbox columna única, `max-width: 520px`
- KPI cards al 100% de ancho, tipografía grande, `border-radius: 16px`
- **Chart.js** para gráficos (CDN). Barras horizontales para rankings. Altura máxima 300px por gráfico.
- Botones y elementos táctiles con `min-height: 44px`
- Todo en un **único archivo `index.html`** (CSS y JS embebidos)

#### ESTRUCTURA DEL DASHBOARD HTML

1. **Header** — nombre real del negocio/dataset + fecha de los datos
2. **KPI cards** — métricas más importantes extraídas del archivo
3. **Gráfico principal** — el que mejor represente los datos encontrados
4. **Gráfico secundario** — comparativo, tendencia o ranking según lo disponible
5. **Tabla resumen** — datos detallados del archivo
6. **Footer** — fuente real del archivo

#### GENERACIÓN DE CÓDIGO PARA VIZ TOOLS

Al generar código para las viz tools, respetar la semántica nativa de cada una:

**Power BI (M + DAX):**
- M code: usar `PostgreSQL.Database()` como función de conexión
- DAX: medidas con `CALCULATE`, `DATEADD`, `DIVIDE` — nunca inventar funciones
- Incluir siempre: Total, MoM Growth, Running Total como medidas base

**Tableau (.tds + LOD):**
- XML `.tds`: respetar schema Tableau — atributos `datatype`, `role`, `type` correctos
- LOD: usar `{ FIXED }`, `{ INCLUDE }`, `{ EXCLUDE }` según el caso
- Incluir siempre: % del total, running sum, rank, window average

**Looker (LookML):**
- Views: `sql_table_name`, dimensions con `sql: ${TABLE}.columna`, measures con `type: sum/count/average`
- `dimension_group` para fechas con `timeframes: [date, week, month, quarter, year]`
- Model: `connection` válido, `include: "views/*.lkml"`

**QuickSight (JSON + sintaxis propia):**
- Manifest JSON: formato exacto con `fileLocations` y `globalUploadSettings`
- Calculated fields: usar `ifelse`, `sumOver`, `periodToDateSum`, `dateDiff`
- IAM Policy: principio de mínimo privilegio — solo permisos necesarios

#### ENTREGABLE PARA DASHBOARDS HTML

- Reemplazar `index.html` en el repositorio
- Commit con mensaje descriptivo
- Push a la branch activa

---

## ANTI-ALUCINACIÓN: LO QUE NUNCA HACER

- No inventar registros, métricas o categorías que no estén en el archivo
- No agregar "datos de ejemplo" si el archivo ya tiene datos reales
- No usar datos de sesiones anteriores en una nueva sesión
- No asumir campos que no se han leído — siempre leer primero
- No avanzar a Fase 2 sin confirmación del usuario en Fase 1
- No inventar funciones DAX, LOD, LookML o QuickSight que no existan en la documentación oficial
- No generar XML `.tds` con atributos inválidos para la versión de Tableau

---

## RECORDATORIO AUTOMÁTICO

Al inicio de cada tarea de dashboard o viz tool:

> "Voy a leer el archivo de datos primero. No construiré nada hasta confirmar los datos contigo."

Al inicio de cada tarea de viz tool setup:

> "Voy a generar el paquete completo para [Tool]. Incluirá: conexión, cálculos semánticos, instrucciones paso a paso y comparativa de costos."
