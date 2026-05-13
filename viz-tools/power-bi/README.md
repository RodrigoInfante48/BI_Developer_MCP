# Power BI — Microsoft Ecosystem

**Tool MCP:** `datapocket_powerbi_setup`  
**Ecosistema:** Microsoft 365 / Azure  
**Costo base:** Power BI Desktop gratis · Pro $10/usuario/mes · Premium desde $20/usuario/mes  
**Estado:** ✅ Implementado

---

## ¿Qué genera este tool?

Dado un conjunto de tablas PostgreSQL, el tool produce todo lo necesario para tener un reporte funcional en Power BI Desktop en menos de 10 minutos.

### 1. Power Query M — Conexión a PostgreSQL

```powerquery
let
    Source = PostgreSQL.Database("localhost:5432", "datapocket"),
    public_ventas = Source{[Schema="public", Item="ventas"]}[Data]
in
    public_ventas
```

Cada tabla recibe su propio bloque M listo para pegar en el **Advanced Editor** (`Home → Transform Data → Advanced Editor`).

### 2. DAX Measures — Starter Kit

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

### 3. Instrucciones de conexión

Paso a paso para conectar Power BI Desktop a PostgreSQL via Npgsql driver (gratis).

### 4. Mobile Layout

Instrucciones para activar **View → Mobile layout** y publicar a Power BI Service con acceso via la app móvil.

---

## Prerrequisitos

| Componente | Costo | Descarga |
|---|---|---|
| Power BI Desktop | Gratis | Microsoft Store / powerbi.microsoft.com |
| Npgsql driver | Gratis | github.com/npgsql/npgsql/releases |
| PostgreSQL corriendo | Gratis | localhost:5432 |

---

## Cómo usar el tool

```
"Conecta Power BI a las tablas ventas, productos y clientes en mi PostgreSQL local"
```

Claude llama a `datapocket_powerbi_setup` y devuelve:
- Código M para las 3 tablas
- 3 medidas DAX de arranque
- Guía paso a paso de conexión

---

## Casos de uso ideales

- **Reportes corporativos** en entornos Microsoft 365
- **Análisis ad-hoc** con slicers y drill-through
- **Dashboards ejecutivos** con scheduled refresh desde Power BI Service
- **Integración con Excel** via Power Query compartido

---

## Archivos de ejemplo

Ver carpeta `examples/` para outputs de muestra generados por el tool.
