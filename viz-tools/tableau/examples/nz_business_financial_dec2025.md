# DataPocket — Tableau Setup
## NZ Business Financial Data · December 2025 Quarter

**Fuente:** Business Data Collection (BDC) — Stats NZ  
**Archivos:** `business-financial-data-december-2025-quarter.csv` (9,315 filas) · `machine-readable-business-employment-data-dec-2025-quarter.csv` (25,672 filas)  
**Período financiero:** Q2 2016 → Q4 2025 · **Período empleo:** Q2 2011 → Q4 2025  
**Unidad:** Millones NZD (Magnitude = 6) · **Industrias Level 1:** 14 sectores NZSIOC

---

## 1. Archivo .tds — Tableau Data Source (CSV)

Guarda como `nz_bdc_financial.tds` y ábrelo directamente en Tableau Desktop.  
Reemplaza `C:/ruta/a/tu/carpeta/` con la ruta real donde tengas el CSV en tu máquina.

```xml
<?xml version='1.0' encoding='utf-8' ?>
<datasource name='nz_bdc_financial'
            caption='NZ Business Financial Data Dec 2025'
            version='18.1'
            inline='true'>

  <connection class='textscan'
              filename='C:/Users/rodrigoi.NICE_SYSTEMS/OneDrive - NiCE Ltd/Desktop/Tableu/business-financial-data-december-2025-quarter.csv'>
    <format character=',' header='yes' locale='en_NZ' />
    <relation name='business-financial-data-december-2025-quarter.csv'
              table='[business-financial-data-december-2025-quarter#csv]'
              type='table' />
  </connection>

  <aliases enabled='yes'/>

  <!-- Dimensiones -->
  <column datatype='string'  name='[Series_reference]' role='dimension' type='nominal'
          caption='Series ID'/>
  <column datatype='real'    name='[Period]'            role='dimension' type='ordinal'
          caption='Period (YYYY.MM)'/>
  <column datatype='string'  name='[STATUS]'            role='dimension' type='nominal'
          caption='Status'/>
  <column datatype='string'  name='[UNITS]'             role='dimension' type='nominal'
          caption='Units'/>
  <column datatype='string'  name='[Subject]'           role='dimension' type='nominal'
          caption='Subject'/>
  <column datatype='string'  name='[Group]'             role='dimension' type='nominal'
          caption='Industry Level (NZSIOC)'/>
  <column datatype='string'  name='[Series_title_1]'    role='dimension' type='nominal'
          caption='Financial Variable'/>
  <column datatype='string'  name='[Series_title_2]'    role='dimension' type='nominal'
          caption='Industry'/>
  <column datatype='string'  name='[Series_title_3]'    role='dimension' type='nominal'
          caption='Price Type'/>
  <column datatype='string'  name='[Series_title_4]'    role='dimension' type='nominal'
          caption='Adjustment Method'/>

  <!-- Medidas -->
  <column datatype='real'    name='[Data_value]'        role='measure'   type='quantitative'
          caption='Value (NZD Millions)'/>
  <column datatype='integer' name='[Magnitude]'         role='measure'   type='quantitative'
          caption='Magnitude'/>

</datasource>
```

> **Nota Mac/Linux:** En `filename` usa barras `/` y la ruta absoluta de tu sistema, por ejemplo `/Users/nombre/data/business-financial-data-december-2025-quarter.csv`

---

## 2. Calculated Fields — LOD Expressions y Table Calculations

Crea cada uno desde **Analysis → Create Calculated Field** en Tableau Desktop.

---

### `[Quarter Date]`
Convierte el campo `Period` (YYYY.MM) a una fecha real usable en ejes temporales.

```tableau
MAKEDATE(
  INT([Period]),
  INT(([Period] - INT([Period])) * 100 + 0.5),
  1
)
```
> Produce fechas como `2025-12-01` para `2025.12`. Usa este campo en lugar de `[Period]` para todos los ejes de tiempo.

---

### `[Year]`
```tableau
INT([Period])
```
> Extrae el año para filtros y agrupaciones anuales.

---

### `[Quarter Label]`
```tableau
"Q" + STR(INT(INT(([Period] - INT([Period])) * 100 + 0.5) / 3 + 0.67))
+ " " + STR(INT([Period]))
```
> Genera etiquetas como `Q4 2025`, `Q1 2025` para visualizaciones.

---

### `[Sales NZD M]`
Extrae solo los valores de Sales (operating income) con método `Current prices, Unadjusted`.

```tableau
IF [Series_title_1] = "Sales (operating income)"
   AND [Series_title_3] = "Current prices"
   AND [Series_title_4] = "Unadjusted"
THEN [Data_value]
END
```

---

### `[Operating Profit NZD M]`
```tableau
IF [Series_title_1] = "Operating profit"
THEN [Data_value]
END
```

---

### `[Salaries NZD M]`
```tableau
IF [Series_title_1] = "Salaries and wages"
THEN [Data_value]
END
```

---

### `[Purchases NZD M]`
```tableau
IF [Series_title_1] = "Purchases and operating expenditure"
THEN [Data_value]
END
```

---

### `[Operating Margin %]` — LOD Fixed
Margen operativo por industria y trimestre, independiente de la granularidad de la vista.

```tableau
{ FIXED [Series_title_2], [Period] :
    SUM(IF [Series_title_1] = "Operating profit" THEN [Data_value] END)
}
/
NULLIF(
  { FIXED [Series_title_2], [Period] :
      SUM(IF [Series_title_1] = "Sales (operating income)"
          AND [Series_title_3] = "Current prices"
          AND [Series_title_4] = "Unadjusted"
          THEN [Data_value] END)
  },
  0
)
```
> Formatea como **Percentage** con 1 decimal. `NULLIF` evita división por cero.

---

### `[Salaries % of Sales]` — LOD Fixed
```tableau
{ FIXED [Series_title_2], [Period] :
    SUM(IF [Series_title_1] = "Salaries and wages" THEN [Data_value] END)
}
/
NULLIF(
  { FIXED [Series_title_2], [Period] :
      SUM(IF [Series_title_1] = "Sales (operating income)"
          AND [Series_title_3] = "Current prices"
          AND [Series_title_4] = "Unadjusted"
          THEN [Data_value] END)
  },
  0
)
```

---

### `[Sales YoY Growth]` — Table Calculation
Crecimiento de Sales respecto al mismo trimestre del año anterior.

```tableau
(SUM([Sales NZD M]) - LOOKUP(SUM([Sales NZD M]), -4))
/ ABS(NULLIF(LOOKUP(SUM([Sales NZD M]), -4), 0))
```
> Requiere que `[Quarter Date]` esté como dimensión de fecha en la vista. `LOOKUP(-4)` apunta 4 trimestres atrás (mismo quarter, año anterior).  
> **Configurar en:** Click derecho sobre la pill → Edit Table Calculation → Compute using: `Quarter Date`

---

### `[Sales Running Total]` — Table Calculation
```tableau
RUNNING_SUM(SUM([Sales NZD M]))
```
> Acumulado corriente dentro de la partición visible. Útil en line charts por industria.

---

### `[Industry Sales Rank]` — LOD
Ranking de industrias por Sales en cada trimestre.

```tableau
RANK_DENSE(
  { FIXED [Series_title_2], [Period] :
      SUM(IF [Series_title_1] = "Sales (operating income)"
          AND [Series_title_3] = "Current prices"
          AND [Series_title_4] = "Unadjusted"
          THEN [Data_value] END)
  }
)
```

---

### `[Sales Moving Avg 4Q]` — Table Calculation
Promedio móvil de 4 trimestres para suavizar estacionalidad.

```tableau
WINDOW_AVG(SUM([Sales NZD M]), -3, 0)
```

---

### `[NZSIOC Level]` — Helper dimension
Clasifica si la fila corresponde a Level 1 o Level 2 de la jerarquía NZSIOC.

```tableau
IF CONTAINS([Group], "Level 1") THEN "Level 1 (Sector)"
ELSEIF CONTAINS([Group], "Level 2") THEN "Level 2 (Industry)"
ELSE "Other"
END
```

---

## 3. Custom SQL — Para usar en New Custom SQL

Agrega en **Data Source** → **New Custom SQL** cuando uses Tableau con un conector SQL sobre los archivos (ej. via Tableau Bridge o una base de datos):

```sql
SELECT
    Period,
    CAST(FLOOR(Period) AS INT)                             AS Year,
    CAST(ROUND((Period - FLOOR(Period)) * 100) AS INT)     AS Month,
    Series_title_1                                          AS Financial_Variable,
    Series_title_2                                          AS Industry,
    Series_title_3                                          AS Price_Type,
    Series_title_4                                          AS Adjustment,
    "Group"                                                 AS NZSIOC_Level,
    Data_value                                              AS Value_NZD_Millions
FROM
    "business-financial-data-december-2025-quarter"
WHERE
    Data_value IS NOT NULL
    AND STATUS = 'F'
ORDER BY
    Period ASC,
    Series_title_2 ASC,
    Series_title_1 ASC
```

---

## 4. Recomendaciones de Visualización — Dashboards para este Dataset

| Sheet | Rows | Columns | Marks | Filtros recomendados |
|---|---|---|---|---|
| **Sales por Industria Q4 2025** | `Industry` | `SUM(Sales NZD M)` | Bar horizontal | `Period = 2025.12` · `NZSIOC Level = Level 1` · `Price Type = Current prices` · `Adjustment = Unadjusted` |
| **Tendencia histórica de Sales** | `Quarter Date` | `SUM(Sales NZD M)` | Line, color=`Industry` | `NZSIOC Level = Level 1` · `Unadjusted` |
| **Operating Margin % por sector** | `Industry` | `AVG(Operating Margin %)` | Bar horizontal, color rojo→verde | `Period = 2025.12` |
| **Mapa de calor Industria × Año** | `Industry` | `Year` | Square, color=`SUM(Sales NZD M)` | `NZSIOC Level = Level 1` |
| **YoY Growth por sector** | `Quarter Date` | `Sales YoY Growth` | Line, color=`Industry` | `Year >= 2017` (necesita año anterior) |
| **Salaries % of Sales** | `Industry` | `AVG(Salaries % of Sales)` | Bar horizontal | `Period = 2025.12` |
| **Scatter: Margin vs Sales** | `AVG(Operating Margin %)` | `SUM(Sales NZD M)` | Circle, size=`SUM(Salaries NZD M)` | `NZSIOC Level = Level 1` · `Period = 2025.12` |

### Top insights para destacar en el dashboard:
- **Wholesale Trade** lidera en Sales: **$43,002M** en Q4 2025
- **Professional Services** tiene el mayor Operating Profit: **$4,829M**
- **Rental & Real Estate**: segundo mayor profit con **$3,914M**, volumen bajo → margen alto
- **Retail Trade & Accommodation**: alto volumen de compras ($26,747M) → margen comprimido
- **Manufacturing**: salarios más altos ($5,252M) como % de sales

---

## 5. Instrucciones Paso a Paso

### Opción A — Tableau Public (GRATIS)

1. Descarga **Tableau Public** desde `public.tableau.com` → botón "Download Tableau Public"
2. Abre Tableau Public → **Connect** → **Text File**
3. Navega hasta `business-financial-data-december-2025-quarter.csv` y selecciónalo
4. En la pestaña **Data Source** verás las columnas. Revisa que `Data_value` sea `#` (número)
5. Ve a **Sheet 1** (tab inferior izquierdo)
6. En el panel izquierdo, arrastra `Series_title_2` (Industry) a **Rows**
7. Arrastra `Data_value` a **Columns** → Tableau sumará automáticamente → `SUM(Data_value)`
8. Arrastra `Series_title_1` (Financial Variable) a **Filters** → selecciona `Sales (operating income)`
9. Clic derecho en el eje → **Sort Descending** → tienes tu ranking de industrias
10. Para crear calculated fields: menú **Analysis → Create Calculated Field** → pega cualquier fórmula de la sección 2
11. Para publicar: **File → Save to Tableau Public As...** → inicia sesión o crea cuenta gratuita

### Opción B — Tableau Desktop (Trial 14 días / Licencia)

1. Descarga Tableau Desktop desde `tableau.com/products/desktop`
2. Abre el archivo `nz_bdc_financial.tds` (de la sección 1) directamente desde tu sistema de archivos
3. Tableau abrirá la conexión al CSV automáticamente
4. Crea los calculated fields de la sección 2 desde **Analysis → Create Calculated Field**
5. Para el campo `[Quarter Date]`: clic derecho en `Period` en el panel izquierdo → **Create** → **Calculated Field**
6. Una vez creado `[Quarter Date]`, arrástralo al eje de tiempo y selecciona granularidad **Quarter**
7. Aplica los filtros: `[NZSIOC Level]` = `Level 1`, `[Series_title_4]` = `Unadjusted` para datos limpios
8. Para publicar en Tableau Server/Online: **Server → Publish Workbook**

### Tip de filtros obligatorios
Dado que el dataset tiene múltiples ajustes para el mismo dato (Unadjusted / Seasonally adjusted / Trend), **siempre filtra por `Series_title_4`** antes de visualizar Sales para evitar triplicar los valores sumados.

---

## 6. Costos — Comparativa Tableau vs Alternativas

| Plan | Precio | Conecta al CSV | Publica | Notas |
|---|---|---|---|---|
| **Tableau Public** | **$0** | Sí (Text File) | Sí (galería pública) | Datos deben ser públicos — ideal para este dataset de Stats NZ |
| **Tableau Creator** | **$75/user/mes** | Sí (todas las fuentes) | Server/Online | Desktop + Server incluidos |
| **Tableau Explorer** | **$42/user/mes** | Solo via Bridge | Web only | Requiere 1 Creator en el org |
| **Tableau Viewer** | **$15/user/mes** | No | Solo lectura | Para consumidores del dashboard |
| **Power BI Desktop** | **$0** | Sí (CSV nativo) | Power BI Service ($10/user/mes) | Alternativa gratuita con DAX |
| **Looker Studio** | **$0** | Sí (Google Sheets/CSV upload) | Web público | Gratuito total, menos potente |

> **Stack $0 recomendado para este dataset:**  
> Los datos son públicos de Stats NZ → Tableau Public es la opción ideal.  
> Descarga → conecta al CSV → crea las vizs de la sección 4 → publica con un link público.

> **Si necesitas datos privados o conexión a base de datos:**  
> Tableau Creator ($75/user/mes) o Power BI Pro ($10/user/mes con Desktop gratis).

---

## 7. Estructura del Workbook Sugerida

```
NZ Business Financial Data — Tableau Workbook
│
├── Data Sources
│   ├── nz_bdc_financial (CSV financiero)
│   └── nz_bdc_employment (CSV empleo — join opcional por Industry+Period)
│
├── Sheets
│   ├── 01_Sales_Ranking_Q4_2025      ← Bar horizontal por industria
│   ├── 02_Sales_Trend_2016_2025      ← Line chart temporal
│   ├── 03_Operating_Margin_Heatmap   ← Square marks, color por margen
│   ├── 04_YoY_Growth_Waterfall       ← Bar chart growth %
│   ├── 05_Salaries_vs_Sales_Scatter  ← Scatter por industria
│   └── 06_COVID_Impact_2020          ← Filtro Year IN (2019,2020,2021)
│
└── Dashboard
    └── NZ_BDC_Executive_Summary      ← Layout con los 6 sheets
```

---

*Generado por DataPocket MCP · Fuente: Stats NZ Business Data Collection Q4 2025*
