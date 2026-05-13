# Tableau — Salesforce Ecosystem

**Tool MCP:** `datapocket_tableau_setup`  
**Ecosistema:** Salesforce  
**Costo base:** Tableau Public gratis (datos públicos) · Creator $75/usuario/mes · Explorer $42/usuario/mes  
**Estado:** 🔜 Próxima implementación

---

## ¿Qué generará este tool?

Dado un conjunto de tablas PostgreSQL, el tool producirá todo lo necesario para conectar y visualizar en Tableau Desktop o Tableau Public.

### 1. Tableau Data Source (.tds)

Archivo XML listo para abrir en Tableau Desktop — con la conexión PostgreSQL ya configurada, aliases de columnas y tipos de datos inferidos.

```xml
<?xml version='1.0' encoding='utf-8' ?>
<datasource name='ventas' inline='true' source-platform='win'>
  <connection class='postgres' dbname='datapocket' port='5432' server='localhost'>
    <relation name='ventas' table='[public].[ventas]' type='table' />
  </connection>
  <column datatype='integer' name='[id]' role='dimension' type='ordinal' />
  <column datatype='real' name='[revenue]' role='measure' type='quantitative' />
  <column datatype='date' name='[fecha]' role='dimension' type='ordinal' />
</datasource>
```

### 2. Calculated Fields — Equivalente a DAX

```
// % del total (LOD Fixed)
{ FIXED [categoria] : SUM([revenue]) } / TOTAL(SUM([revenue]))

// Running Total
RUNNING_SUM(SUM([revenue]))

// Moving Average 3 períodos
WINDOW_AVG(SUM([revenue]), -2, 0)

// YoY Growth
(SUM([revenue]) - LOOKUP(SUM([revenue]), -12)) / ABS(LOOKUP(SUM([revenue]), -12))

// Rank dentro de dimensión
RANK_DENSE(SUM([revenue]))
```

### 3. Custom SQL para conexión

Query optimizado para usar en `New Custom SQL` de Tableau — útil cuando se necesitan joins o transformaciones que Tableau Prep no puede hacer.

### 4. Recomendaciones de Viz por tipo de dato

| Tipo de columna | Viz recomendada |
|---|---|
| Fecha + numérico | Line chart con forecast |
| Categoría + numérico | Horizontal bar (ranking) |
| Geo + numérico | Filled map |
| Dos numéricos | Scatter plot |
| Parte/todo | Treemap o pie |

---

## Prerrequisitos

| Componente | Costo | Notas |
|---|---|---|
| Tableau Desktop | $75/usuario/mes | 14 días trial gratis |
| Tableau Public | Gratis | Datos son públicos — no usar datos sensibles |
| PostgreSQL JDBC driver | Gratis | Para conexión desde Tableau |

---

## Diferencias clave vs Power BI

| Aspecto | Power BI | Tableau |
|---|---|---|
| ETL / transformación | Power Query M | Tableau Prep (pago) / Custom SQL |
| Lenguaje de cálculo | DAX | LOD Expressions |
| Archivo de conexión | Nativo via Npgsql | `.tds` XML |
| Versión gratuita | Desktop gratis, Service pago | Public gratis (datos públicos) |
| Fortaleza | Ecosistema Microsoft | Viz interactiva avanzada |

---

## Casos de uso ideales

- **Exploración visual avanzada** con drag-and-drop intuitivo
- **Dashboards públicos** via Tableau Public (portfolios, datos abiertos)
- **Análisis geoespacial** con mapas nativos
- **Entornos Salesforce** con integración CRM

---

## Archivos de ejemplo

Ver carpeta `examples/` para outputs de muestra una vez implementado el tool.
