# Ejemplo de Output — `datapocket_powerbi_setup` con tabla `ventas`

**Input utilizado:**
```python
{
  "table_names": ["ventas"],
  "schema_name": "public",
  "pg_host": "localhost",
  "pg_port": "5432",
  "pg_database": "datapocket"
}
```

Columnas de la tabla hipotética `ventas`: `id`, `fecha`, `categoria`, `revenue`, `region`

---

# ⚡ DataPocket — Power BI Setup

## Prerequisites
1. **Power BI Desktop** (free): [Download](https://powerbi.microsoft.com/desktop/)
2. **Npgsql driver** para PostgreSQL: [Download](https://github.com/npgsql/npgsql/releases)
3. PostgreSQL corriendo en `localhost:5432`

## Step-by-Step Connection
1. Abre **Power BI Desktop**
2. Click **Get Data** → **Database** → **PostgreSQL database**
3. Server: `localhost:5432` · Database: `datapocket`
4. Selecciona **DirectQuery** para tiempo real o **Import** para snapshots
5. Selecciona la tabla `ventas` y click **Load**

---

## Power Query M Code (Advanced Editor)
Usa en **Home → Transform Data → Advanced Editor**:

### Table: `ventas`
```powerquery
let
    Source = PostgreSQL.Database("localhost:5432", "datapocket"),
    public_ventas = Source{[Schema="public", Item="ventas"]}[Data]
in
    public_ventas
```

---

## DAX Measures (Starter Kit)
Crea estas medidas en **Modeling → New Measure**:

```dax
// Total Revenue
Total Revenue = SUM('ventas'[revenue])

// Month-over-Month Growth
MoM Growth =
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)

// Running Total
Running Total = CALCULATE([Total Revenue], FILTER(ALL('Calendar'[Date]), 'Calendar'[Date] <= MAX('Calendar'[Date])))
```

### Medidas adicionales sugeridas para `ventas`

```dax
// Revenue por Categoría
Revenue por Categoria =
CALCULATE([Total Revenue], ALLEXCEPT('ventas', 'ventas'[categoria]))

// Top 3 Regiones
Top Regiones =
RANKX(ALL('ventas'[region]), [Total Revenue], , DESC, DENSE)

// % del Total
Pct del Total =
DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL('ventas')))
```

---

## Recomendaciones de Visualización

| Campo | Viz Recomendada | Notas |
|---|---|---|
| `fecha` + `revenue` | Line Chart | Evolución temporal de ingresos |
| `categoria` + `SUM(revenue)` | Clustered Bar Chart | Ranking de categorías |
| `region` + `SUM(revenue)` | Map / Filled Map | Distribución geográfica |
| `categoria` + `region` | Matrix / Heatmap | Cruce multidimensional |
| KPIs (`Total Revenue`, `MoM Growth`) | Card | Panel de indicadores clave |

---

## Mobile Layout
1. **View** → **Mobile layout**
2. Arrastra los visuales al canvas de teléfono
3. Publica en **Power BI Service** (gratis con cuenta work/school)
4. Accede desde **Power BI Mobile app**

---

## Costos — Power BI vs Alternativas

| Plan | Precio | Características principales |
|---|---|---|
| **Power BI Desktop** | **$0** | Conexión directa a PostgreSQL, DAX completo, sin límite de datos local |
| **Power BI Pro** | **$10/user/mes** | Compartir dashboards, colaboración en equipo |
| **Power BI Premium** | **$20/user/mes** | Capacidad dedicada, paginación, AI features |
| Tableau Creator | $75/user/mes | Alternativa — mayor costo |
| Looker | $3,000+/mes | Alternativa empresarial |

> 💡 **Stack $0**: PostgreSQL + Python + Power BI Desktop = cero costo de licencia.
> 🎯 Para publicar y compartir: Power BI Pro ($10/user/mes) es la opción más económica del mercado.
