# Ejemplo de Output — `datapocket_tableau_setup` con tabla `ventas`

**Input utilizado:**
```python
{
  "table_names": ["ventas"],
  "schema_name": "public",
  "pg_host": "localhost",
  "pg_port": "5432",
  "pg_database": "datapocket",
  "date_column": "fecha",
  "measure_columns": ["revenue"],
  "dimension_columns": ["categoria", "region"]
}
```

Columnas de la tabla hipotética `ventas`: `id`, `fecha`, `categoria`, `revenue`, `region`

---

# 📊 DataPocket — Tableau Setup

## Tablas: `ventas`
- **Host**: `localhost:5432` · **Database**: `datapocket` · **Schema**: `public`
- **Fecha**: `fecha` · **Medidas**: `revenue`
- **Dimensiones**: `categoria`, `region`

---

## 1. Archivo .tds (Tableau Datasource XML)
Guarda como `ventas.tds` y ábrelo directamente en Tableau Desktop:

```xml
<?xml version='1.0' encoding='utf-8' ?>
<workbook source-build='2024.1' source-platform='linux' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <!-- Datasource: ventas -->
  <datasource caption='ventas' name='ventas' version='18.1'>
    <connection authentication='username-password'
                class='postgres'
                dbname='datapocket'
                port='5432'
                server='localhost'
                username='datapocket_user'>
      <relation name='ventas' table='[public].[ventas]' type='table'/>
    </connection>
    <aliases enabled='yes'/>
      <column datatype="real" name="[revenue]" role="measure" type="quantitative"/>
      <column datatype="string" name="[categoria]" role="dimension" type="nominal"/>
      <column datatype="string" name="[region]" role="dimension" type="nominal"/>
      <column datatype="date" name="[fecha]" role="dimension" type="ordinal"/>
  </datasource>
</workbook>
```

---

## 2. Calculated Fields (sintaxis Tableau nativa)
Crea estos campos en **Analysis → Create Calculated Field**:

### `% del Total por Dimensión`
```tableau
{ FIXED [categoria] : SUM([revenue]) } / TOTAL(SUM([revenue]))
```
> LOD Expression — porcentaje que representa cada dimensión sobre el total

### `Running Total`
```tableau
RUNNING_SUM(SUM([revenue]))
```
> Acumulado corriente — requiere Table Calculation sobre la vista

### `Moving Average 3 Períodos`
```tableau
WINDOW_AVG(SUM([revenue]), -2, 0)
```
> Promedio móvil de 3 períodos — suaviza variaciones estacionales

### `Rank Dense`
```tableau
RANK_DENSE(SUM([revenue]))
```
> Ranking denso sin huecos entre posiciones iguales

### `YoY Growth (Year-over-Year)`
```tableau
(SUM([revenue]) - LOOKUP(SUM([revenue]), -12)) / ABS(LOOKUP(SUM([revenue]), -12))
```
> Crecimiento año sobre año usando LOOKUP(-12) — requiere `[fecha]` como dimensión de fecha en la vista

> ⚠️  YoY Growth requiere que `[fecha]` esté como dimensión **mensual** en la vista para que LOOKUP(-12) apunte al mismo mes del año anterior.

---

## 3. Custom SQL — New Custom SQL
Pega en **Data Source** → **New Custom SQL**:

```sql
SELECT
  public.ventas.categoria,
  public.ventas.region,
  public.ventas.fecha,
  SUM(public.ventas.revenue) AS total_revenue
FROM public.ventas
GROUP BY
  public.ventas.categoria,
  public.ventas.region,
  public.ventas.fecha
ORDER BY
  public.ventas.fecha ASC
```

---

## 4. Recomendaciones de Visualización

| Tipo de Columna | Viz Recomendada en Tableau | Notas |
| --- | --- | --- |
| Dimensión (string) | Bar Chart, Treemap, Highlight Table | Arrastra a Rows/Columns |
| Medida (número) | Bar Chart, Line Chart, Scatter Plot | Arrastra a Columns/Rows |
| Fecha (date) | Line Chart de series temporales | Usa granularidad Month/Quarter |
| Fecha + Medida | Dual-Axis Line, Area Chart | Click derecho → Dual Axis |
| Dimensión + Medida | Horizontal Bar (ranking) | Sort descending para top-N |
| Dos Medidas | Scatter Plot | Detecta correlaciones |
| Geográfica (país/región) | Map (Filled Map) | Requiere role='Geographic' |
| Jerarquía | Treemap, Sunburst (extensión) | Drill-down nativo con + |

**Vizs sugeridas para `ventas`:**
- `fecha` + `revenue` → **Line Chart** (evolución temporal de ingresos)
- `categoria` + `SUM(revenue)` → **Horizontal Bar Chart** (ranking de categorías)
- `region` + `SUM(revenue)` → **Filled Map** (si region tiene valores geográficos) o **Bar Chart**
- `categoria` + `region` + `SUM(revenue)` → **Highlight Table / Heatmap**

---

## 5. Instrucciones de Conexión

### Tableau Desktop
1. Abre **Tableau Desktop** → **Connect** → **To a Server** → **PostgreSQL**
2. Server: `localhost` · Port: `5432` · Database: `datapocket`
3. Authentication: Username/Password (usuario: `datapocket_user`)
4. Selecciona el schema `public` y arrastra la tabla `ventas`
5. Para usar Custom SQL: **New Custom SQL** → pega el query de la sección anterior
6. Guarda el datasource como `ventas.tds` para reutilizar
7. Publica en **Tableau Server/Online**: Server → Publish Workbook

### Tableau Public (gratuito)
1. Descarga **Tableau Public** (gratis) desde public.tableau.com
2. **Connect** → **Text file** o **Excel** (Tableau Public NO conecta a PostgreSQL directamente)
3. Alternativa: Exporta tu query de PostgreSQL como CSV → Conéctate al CSV
4. Diseña tu viz y publica gratis en Tableau Public Gallery

---

## 6. Costos — Tableau Public vs Licencias

| Plan | Precio | Características principales | Limitaciones |
| --- | --- | --- | --- |
| **Tableau Public** | **$0** | Todas las vizs, publicación pública | Sin PostgreSQL directo, datos públicos |
| **Tableau Creator** | **$75/user/mes** | Desktop + Server, todas las fuentes | Precio por usuario |
| **Tableau Explorer** | **$42/user/mes** | Solo web, sin Desktop | Requiere al menos 1 Creator |
| **Tableau Viewer** | **$15/user/mes** | Solo lectura de dashboards | Sin edición |

> 💡 **Stack $0**: Exporta tu data a CSV con `datapocket_export` → carga en Tableau Public → comparte el link.
> 🎯 **Alternativa gratuita**: Power BI Desktop ($0) conecta directo a PostgreSQL — usa `datapocket_powerbi_setup`.
