<div align="center">

# 📱 DataPocket MCP

### Sube tu data. Claude te arma el reporte. En cualquier viz tool.

[![Stack](https://img.shields.io/badge/Stack-Python%20+%20PostgreSQL-38bdf8?style=flat-square)](.)
[![Licencias](https://img.shields.io/badge/Licencias-$0%20USD-34d399?style=flat-square)](.)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-Ready-a78bfa?style=flat-square)](https://modelcontextprotocol.io)
[![Version](https://img.shields.io/badge/Version-3.0.0-fb923c?style=flat-square)](.)
[![Tests](https://img.shields.io/badge/Tests-29%20passing-22c55e?style=flat-square)](./tests/test_datapocket.py)

</div>

---

<div align="center">

![DataPocket — De CSV a Dashboard en cualquier Viz Tool](./assets/hero-mockup.svg)

</div>

---

## ¿Qué es DataPocket MCP?

**Un agente de BI universal.** Sube cualquier archivo de datos y Claude genera el paquete completo de conexión, transformación y analítica para la viz tool que uses — Power BI, Tableau, Looker o QuickSight.

```
Tú:     "Aquí están mis ventas del trimestre" [pegas CSV]
Claude: Analiza → Limpia → Carga en PostgreSQL → Genera paquete para tu viz tool
Tú:     Abres el reporte en tu herramienta favorita → Listo
```

**Sin código. Sin licencias adicionales. Sin setup complejo.**

---

## Viz Tools soportadas

| Ecosistema | Viz Tool | Qué genera DataPocket | Estado |
|---|---|---|---|
| **Microsoft** | Power BI Desktop | Código M (Power Query) + medidas DAX | ✅ Activo |
| **Salesforce** | Tableau Desktop / Public | Archivo `.tds` + LOD expressions + Custom SQL | ✅ Activo |
| **Google** | Looker (Enterprise) | LookML completo (view + explore + model) | ✅ Activo |
| **Amazon** | QuickSight | Manifest JSON + dataset config + calculated fields + IAM policy | ✅ Activo |

> Cada tool genera un **paquete completo**: conexión + semántica/cálculos + instrucciones paso a paso + comparativa de costos.

---

## Formatos de entrada soportados

| Formato | Extensión | Detección |
|---------|-----------|-----------|
| CSV | `.csv` | Automática |
| TSV | `.tsv` | Automática |
| JSON Array | `.json` | Automática |
| JSON Lines | `.jsonl` | Automática |
| Excel | `.xlsx` | Por path o base64 |
| SQL Results | — | Pega desde psql/DBeaver |

---

## Tools MCP incluidos

| Tool | Qué hace | Output |
|------|----------|--------|
| `datapocket_ingest_data` | Perfila data, infiere tipos, genera SQL para PostgreSQL | Reporte + CREATE TABLE + INSERT |
| `datapocket_transform` | Filtra, agrega, ordena, pivota datos | Data transformada + código Python |
| `datapocket_generate_dashboard` | Dashboard HTML mobile-first con Chart.js | Archivo `index.html` |
| `datapocket_query_to_dashboard` | Resultados SQL → dashboard automático | Archivo `index.html` |
| `datapocket_powerbi_setup` | Conexión Power BI a PostgreSQL | Código M + medidas DAX starter |
| `datapocket_tableau_setup` | Conexión Tableau a PostgreSQL | `.tds` XML + 6 LOD expressions |
| `datapocket_looker_setup` | Modelo LookML para Looker | view + explore + model `.lkml` + PDT |
| `datapocket_quicksight_setup` | Conexión QuickSight (S3/RDS/Athena) | Manifest JSON + dataset config + IAM policy |
| `datapocket_export` | Exporta datos a CSV, JSON, JSONL, SQL, Markdown | Archivo en formato elegido |

---

## Estructura del repositorio

```
datapocket-mcp/
├── src/
│   └── datapocket_mcp.py          ← MCP Server — todos los tools
│
├── viz-tools/                     ← Paquetes por ecosistema
│   ├── power-bi/                  ← Microsoft
│   │   ├── README.md              ← Guía Power BI + ejemplos de output
│   │   └── examples/              ← Outputs generados de muestra
│   ├── tableau/                   ← Salesforce
│   │   ├── README.md              ← Guía Tableau + ejemplos de output
│   │   └── examples/
│   ├── looker/                    ← Google
│   │   ├── README.md              ← Guía Looker + ejemplos LookML
│   │   └── examples/
│   └── quicksight/                ← Amazon
│       ├── README.md              ← Guía QuickSight + ejemplos JSON
│       └── examples/
│
├── examples/                      ← Datos de prueba compartidos
│   ├── ventas_ejemplo.csv
│   ├── finanzas_ejemplo.csv
│   ├── ejemplo.json
│   ├── ejemplo.jsonl
│   └── ejemplo.tsv
│
├── assets/
│   └── hero-mockup.svg
├── tests/
│   └── test_datapocket.py
├── CLAUDE.md                      ← Reglas de comportamiento del agente
├── pyproject.toml
└── requirements.txt
```

---

## Cómo funciona

### Paso 1 — Tú subes tu data

```
Tú: Analiza estos datos y crea el reporte para Power BI

nombre,ventas,mes,region
Producto A,12400,Enero,Norte
Producto B,9800,Enero,Sur
```

### Paso 2 — Claude perfila y confirma

```
Archivo: ventas.csv
Columnas: nombre (VARCHAR), ventas (BIGINT), mes (VARCHAR), region (VARCHAR)
Registros: 6 | Nulls: 0%
Insights: Producto A supera a B en todas las regiones. Norte lidera.

Solo usaré estos datos. ¿Procedo?
```

### Paso 3 — Claude genera el paquete completo

Para Power BI:
- Código M listo para Advanced Editor
- 3 medidas DAX de arranque (Total, MoM Growth, Running Total)
- Guía de conexión PostgreSQL → Power BI Desktop

Para Tableau:
- Archivo `.tds` XML listo para abrir en Tableau Desktop
- 6 calculated fields LOD para análisis inmediato (% total, running sum, rank, window avg, YoY, FIXED)
- Custom SQL optimizado

Para Looker:
- `view.lkml` con dimensions y measures inferidos de los datos
- `explore.lkml` y `model.lkml` completos
- PDT para agregaciones pre-calculadas

Para QuickSight:
- Manifest JSON para importar desde S3
- Dataset configuration JSON para la API
- IAM policy mínima + comandos CLI `aws quicksight`

---

## Setup en 3 minutos

### 1. Instala dependencias

```bash
pip install mcp pydantic httpx openpyxl chardet
```

### 2. Configura Claude Desktop

Agrega a `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "datapocket": {
      "command": "python",
      "args": ["src/datapocket_mcp.py"],
      "env": {
        "DATAPOCKET_PG_HOST": "localhost",
        "DATAPOCKET_PG_PORT": "5432",
        "DATAPOCKET_PG_DB": "datapocket",
        "DATAPOCKET_PG_USER": "postgres",
        "DATAPOCKET_PG_PASSWORD": "tu_password"
      }
    }
  }
}
```

### 3. Habla con Claude

```
"Aquí están mis datos de ventas [CSV].
 Crea el reporte para Tableau / Power BI / Looker / QuickSight."
```

---

## Comparativa de costos por ecosistema

| Ecosistema | Tool | Costo mínimo | Mejor para |
|---|---|---|---|
| **Microsoft** | Power BI Desktop | $0 (Desktop gratis) | Entornos Microsoft 365 |
| **Salesforce** | Tableau Public | $0 (datos públicos) | Viz interactiva avanzada |
| **Salesforce** | Tableau Creator | $75/usuario/mes | Dashboards empresariales |
| **Google** | Looker Studio | $0 | Dashboards rápidos con BigQuery |
| **Google** | Looker Enterprise | $3,000+/mes | Data governance enterprise |
| **Amazon** | QuickSight Reader | $0.30/sesión | Muchos viewers, pocos autores |
| **Amazon** | QuickSight Author | $18/usuario/mes | Stack AWS nativo |

> DataPocket MCP: **$0** — solo necesitas la herramienta que ya tienes.

---

## Stack técnico (todo gratis)

```
┌──────────────┐     ┌────────────────┐     ┌─────────────────────────────┐
│  Tu data     │────▶│  Claude +      │────▶│  Power BI  │ Tableau        │
│  CSV / JSON  │     │  DataPocket    │     │  Looker    │ QuickSight      │
│  SQL Results │     │  MCP v3        │     └─────────────────────────────┘
└──────────────┘     └───────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              ┌─────▼─────┐   ┌──────▼──────┐
              │ PostgreSQL │   │  Dashboard  │
              │ (gratuito) │   │  HTML       │
              └────────────┘   └─────────────┘
```

---

## Roadmap

| Versión | Tool | Estado |
|---|---|---|
| v2.0 | Core MCP (ingest, transform, dashboard, Power BI, export) | ✅ Lanzado |
| v3.1 | `datapocket_tableau_setup` | ✅ Lanzado |
| v3.2 | `datapocket_looker_setup` | ✅ Lanzado |
| v3.3 | `datapocket_quicksight_setup` | ✅ Lanzado |
| v3.4 | `datapocket_metabase_setup` (open source) | 💡 Considerado |
| v3.5 | `datapocket_superset_setup` (Apache, open source) | 💡 Considerado |

---

## FAQ

**¿Necesito saber programar?**
No. Tú hablas con Claude en español. Claude hace todo.

**¿Necesito instalar PostgreSQL?**
Solo si quieres guardar los datos permanentemente. Para dashboards rápidos, solo pega tu CSV.

**¿Puedo usar esto en el trabajo con Tableau o QuickSight?**
Sí. El código generado (`.tds`, LookML, manifest JSON) es compatible con las versiones comerciales de cada tool.

**¿Funciona con datos sensibles?**
DataPocket corre 100% local. Tus datos nunca salen de tu máquina salvo cuando los cargas tú mismo en la viz tool.

**¿Puedo contribuir?**
Sí. Ver `viz-tools/` — cada carpeta documenta qué genera el tool correspondiente.

---

<div align="center">

**Hecho por [DailyDuty](https://github.com/RodrigoInfante48) — Instituto para el Desarrollo Diario**

*De datos crudos a decisiones inteligentes. En tu viz tool favorita. Gratis.*

</div>
