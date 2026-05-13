# Looker — Google Ecosystem

**Tool MCP:** `datapocket_looker_setup`  
**Ecosistema:** Google Cloud  
**Costo base:** Looker (Enterprise) desde $3,000/mes · Looker Studio gratis  
**Estado:** 🔜 Próxima implementación

---

## ¿Qué generará este tool?

LookML completo listo para pegar en un proyecto Looker — los 3 archivos que definen el modelo semántico de datos.

### 1. View LookML (`view.lkml`)

```lookml
view: ventas {
  sql_table_name: public.ventas ;;

  dimension: id {
    primary_key: yes
    type: number
    sql: ${TABLE}.id ;;
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

  measure: total_revenue {
    type: sum
    sql: ${TABLE}.revenue ;;
    value_format_name: usd
  }

  measure: avg_revenue {
    type: average
    sql: ${TABLE}.revenue ;;
    value_format_name: usd
  }

  measure: count {
    type: count
    drill_fields: [id, categoria, fecha_date]
  }
}
```

### 2. Explore LookML (`explore.lkml`)

```lookml
explore: ventas {
  label: "Ventas"
  description: "Análisis de ventas por categoría y período"

  join: clientes {
    type: left_outer
    sql_on: ${ventas.cliente_id} = ${clientes.id} ;;
    relationship: many_to_one
  }
}
```

### 3. Model LookML (`model.lkml`)

```lookml
connection: "datapocket_pg"

include: "views/*.lkml"

explore: ventas {}
```

### 4. PDT — Persistent Derived Table

Para agregaciones pre-calculadas que mejoran performance en tablas grandes:

```lookml
view: ventas_summary {
  derived_table: {
    sql:
      SELECT
        categoria,
        DATE_TRUNC('month', fecha) AS mes,
        SUM(revenue)              AS total_revenue,
        COUNT(*)                  AS num_transacciones
      FROM public.ventas
      GROUP BY 1, 2
    ;;
    persist_for: "24 hours"
  }
}
```

---

## Prerrequisitos

| Componente | Costo | Notas |
|---|---|---|
| Looker Enterprise | $3,000+/mes | GCP-hosted o self-hosted |
| Looker Studio | Gratis | Visualización solo, sin LookML |
| Git repo para LookML | Gratis | GitHub/GitLab para version control |

---

## Diferencias clave vs Power BI

| Aspecto | Power BI | Looker |
|---|---|---|
| Modelo semántico | DAX + tablas relacionales | LookML (code-first) |
| ETL | Power Query M | dbt / SQL puro |
| Control de versiones | Limitado | Git nativo |
| Curva de aprendizaje | Media | Alta (LookML) |
| Fortaleza | Self-service rápido | Governance de datos enterprise |

---

## Looker Studio vs Looker

> **Looker Studio** (antes Data Studio) es gratis pero no usa LookML.  
> Genera consultas SQL directas a BigQuery o PostgreSQL y los dashboards son más simples.  
> Este tool genera LookML para **Looker Enterprise** (la versión de pago completa).

---

## Casos de uso ideales

- **Data governance enterprise** — modelo semántico centralizado, una sola fuente de verdad
- **Entornos GCP** con BigQuery como DWH
- **Equipos de datos maduros** con ingenieros dedicados a mantener el modelo
- **Self-service analytics** con métricas controladas por el equipo de datos

---

## Archivos de ejemplo

Ver carpeta `examples/` para outputs de muestra una vez implementado el tool.
