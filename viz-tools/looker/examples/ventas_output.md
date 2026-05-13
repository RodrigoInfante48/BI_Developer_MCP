# Ejemplo de Output — `datapocket_looker_setup` con tablas `ventas` y `productos`

**Input utilizado:**
```python
{
  "table_names": ["ventas", "productos"],
  "schema_name": "public",
  "pg_host": "localhost",
  "pg_port": "5432",
  "pg_database": "datapocket",
  "project_name": "datapocket",
  "primary_table": "ventas",
  "date_column": "fecha"
}
```

Columnas de la tabla hipotética `ventas`: `id`, `fecha`, `nombre`, `categoria`, `monto`
Columnas de la tabla hipotética `productos`: `id`, `fecha`, `nombre`, `categoria`, `monto`

---

# 🔍 DataPocket — Looker LookML Setup

## Tablas: `ventas`, `productos`
- **Host**: `localhost:5432` · **Database**: `datapocket` · **Schema**: `public`
- **Proyecto**: `datapocket` · **Explore principal**: `ventas`
- **Columna de fecha**: `fecha`
- **Joins**: `productos` → `ventas` (left_outer, many_to_one)

---

## 1. view.lkml — Vistas por tabla
Guarda en `views/<tabla>.view.lkml`:

```lookml
view: ventas {
  sql_table_name: "public"."ventas" ;;

  dimension: id {
    type: number
    primary_key: yes
    sql: ${TABLE}.id ;;
    description: "Primary key — replace with the actual PK column name if different."
  }

  dimension: nombre {
    type: string
    sql: ${TABLE}.nombre ;;
    description: "String dimension — duplicate this block for each categorical column."
  }

  dimension: categoria {
    type: string
    sql: ${TABLE}.categoria ;;
  }

  dimension_group: fecha {
    type: time
    timeframes: [date, week, month, quarter, year]
    datatype: date
    sql: ${TABLE}.fecha ;;
  }

  measure: count {
    type: count
    drill_fields: [id, nombre]
  }

  measure: total_monto {
    type: sum
    sql: ${TABLE}.monto ;;
    value_format_name: decimal_2
    description: "Sum — duplicate this block for each numeric column; rename total_<col>."
  }

  measure: avg_monto {
    type: average
    sql: ${TABLE}.monto ;;
    value_format_name: decimal_2
    description: "Average — duplicate this block for each numeric column; rename avg_<col>."
  }
}

view: productos {
  sql_table_name: "public"."productos" ;;

  dimension: id {
    type: number
    primary_key: yes
    sql: ${TABLE}.id ;;
    description: "Primary key — replace with the actual PK column name if different."
  }

  dimension: nombre {
    type: string
    sql: ${TABLE}.nombre ;;
    description: "String dimension — duplicate this block for each categorical column."
  }

  dimension: categoria {
    type: string
    sql: ${TABLE}.categoria ;;
  }

  dimension_group: fecha {
    type: time
    timeframes: [date, week, month, quarter, year]
    datatype: date
    sql: ${TABLE}.fecha ;;
  }

  measure: count {
    type: count
    drill_fields: [id, nombre]
  }

  measure: total_monto {
    type: sum
    sql: ${TABLE}.monto ;;
    value_format_name: decimal_2
    description: "Sum — duplicate this block for each numeric column; rename total_<col>."
  }

  measure: avg_monto {
    type: average
    sql: ${TABLE}.monto ;;
    value_format_name: decimal_2
    description: "Average — duplicate this block for each numeric column; rename avg_<col>."
  }
}
```

---

## 2. explore.lkml — Explore principal
Guarda en `explores/ventas.explore.lkml`:

```lookml
explore: ventas {
  label: "Ventas — DataPocket Explore"
  description: "Main explore for ventas. Rename label to match your business domain."

  join: productos {
    type: left_outer
    relationship: many_to_one
    sql_on: ${ventas.id} = ${productos.id} ;;
  }
}
```

---

## 3. model.lkml — Modelo del proyecto
Guarda como `datapocket.model.lkml`:

```lookml
connection: "datapocket"

include: "views/*.lkml"

explore: ventas {
  label: "Ventas"
}
```

---

## 4. PDT SQL — Tabla derivada pre-calculada
Guarda en `views/ventas_summary.view.lkml`:

```lookml
-- PDT: pre-aggregated summary for ventas
-- Save as views/ventas_summary.lkml

view: ventas_summary {
  derived_table: {
    sql:
      SELECT
        DATE_TRUNC('month', fecha) AS periodo,
        COUNT(*)                   AS total_registros,
        SUM(monto)                 AS total_monto,
        AVG(monto)                 AS avg_monto
      FROM public.ventas
      GROUP BY 1
      ORDER BY 1
    ;;
    persist_for: "24 hours"
  }

  dimension_group: periodo {
    type: time
    timeframes: [month, quarter, year]
    sql: ${TABLE}.periodo ;;
  }

  measure: total_registros {
    type: sum
    sql: ${TABLE}.total_registros ;;
  }

  measure: total_monto {
    type: sum
    sql: ${TABLE}.total_monto ;;
    value_format_name: decimal_2
  }

  measure: avg_monto {
    type: average
    sql: ${TABLE}.avg_monto ;;
    value_format_name: decimal_2
  }
}
```

---

## 5. Instrucciones de Setup

### Crear el proyecto en Looker
1. Ve a **Looker Admin** → **Projects** → **New LookML Project**
2. Nombre del proyecto: `datapocket` · Fuente: **Blank Project**
3. En la configuración de la conexión de la base de datos:
   - **Name**: `datapocket`
   - **Dialect**: PostgreSQL
   - **Host**: `localhost` · **Port**: `5432`
   - **Database**: `datapocket`
   - **Schema**: `public`
4. Crea la estructura de archivos:
   ```
   datapocket/
   ├── datapocket.model.lkml          ← contenido de model.lkml
   ├── views/
   │   ├── ventas.view.lkml           ← view block de la tabla primaria
   │   ├── productos.view.lkml        ← view block de la tabla secundaria
   │   └── ventas_summary.view.lkml   ← PDT (opcional)
   └── explores/
       └── ventas.explore.lkml        ← contenido de explore.lkml
   ```
5. Pega el contenido generado en cada archivo correspondiente
6. Haz clic en **Validate LookML** — corrige cualquier warning antes de hacer deploy
7. **Deploy to Production** cuando el LookML valide sin errores

### Personalizar columnas reales
Reemplaza los nombres de columna de plantilla (`nombre`, `categoria`, `monto`) con
los nombres reales de tu tabla en PostgreSQL.

---

## 6. Costos — Looker Enterprise vs Looker Studio (gratis)

| Plan | Precio estimado | Características | Limitaciones |
| --- | --- | --- | --- |
| **Looker Studio** | **$0** | Dashboards web, conectores nativos (BigQuery, Sheets, etc.) | Sin LookML, sin modelado semántico |
| **Looker Core** | **~$3,000+/mes** (contrato anual) | LookML completo, Git, PDTs, API | Requiere Google Cloud |
| **Looker Enterprise** | **Precio según negociación** | Multi-cloud, HIPAA, SSO avanzado | Contrato mínimo anual |
| **Power BI Desktop** | **$0** | DAX, DirectQuery, tablas relacionales | Solo Windows, sin LookML |
| **Tableau Public** | **$0** | Todas las vizs, publicación pública | Sin PostgreSQL directo |

> 💡 **Stack $0**: Exporta tu data como CSV con `datapocket_export` → carga en **Looker Studio** (gratis) → comparte el link.
> 🎯 **Alternativa gratuita con PostgreSQL directo**: Power BI Desktop ($0) — usa `datapocket_powerbi_setup`.
