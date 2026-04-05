<div align="center">

# 📱 DataPocket MCP

### Sube tu data. Claude te arma el dashboard. Consúltalo en tu celular.

[![Stack](https://img.shields.io/badge/Stack-Python%20+%20PostgreSQL%20+%20Power%20BI-38bdf8?style=flat-square)](.)
[![Costo](https://img.shields.io/badge/Licencias-$0%20USD-34d399?style=flat-square)](.)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-Ready-a78bfa?style=flat-square)](https://modelcontextprotocol.io)

</div>

---

<div align="center">

![DataPocket — De CSV a Dashboard Mobile-First](./assets/hero-mockup.svg)

</div>

---

## ¿Qué obtienes?

**Subes un archivo. Recibes un reporte de inteligencia en tu celular.**

DataPocket MCP convierte a Claude en tu analista de datos personal. Tú hablas, Claude hace todo el trabajo:

```
Tú:     "Aquí están mis ventas del trimestre" [pegas CSV]
Claude: Analiza → Limpia → Carga en PostgreSQL → Genera dashboard
Tú:     Abres el link en tu celular → Toda tu inteligencia en la palma de tu mano
```

**Sin código. Sin licencias. Sin setup complejo.**

---

## Formatos de entrada soportados

| Formato | Ejemplo |
|---------|---------|
| **CSV** | Exporta de Excel, Google Sheets, tu ERP, tu CRM |
| **JSON** | APIs, exports de Notion, Airtable, cualquier sistema |
| **SQL Results** | Copia resultados de pgAdmin, DBeaver, psql |
| **Excel** | Copia las celdas y pégalas como CSV |

---

## Casos de uso reales

### 💰 Inteligencia Financiera Personal

> *"Quiero ver mi portafolio de inversiones en mi celular"*

Pegas tu CSV de transacciones del broker → Claude genera:
- KPIs de patrimonio neto, rendimiento, tasa de ahorro
- Distribución de activos (donut chart)
- Flujo de caja mensual (ingresos vs gastos)
- Rendimiento por instrumento
- Tendencia histórica

---

### 🏪 Dashboard de Negocio / E-commerce

> *"Necesito ver las ventas de hoy desde mi celular"*

Conectas tu PostgreSQL con los datos de ventas → Claude genera:
- Revenue en tiempo real con meta diaria
- Pedidos, ticket promedio, tasa de conversión
- Gráfico de ventas por hora
- Top productos con barras de progreso
- Tabla de últimos pedidos

---

### 🐾 CRM y Seguimiento de Leads

> *"Tengo 500 prospectos en mi base, quiero ver el funnel"*

Exportas tu CRM como CSV → Claude genera:
- Funnel de ventas (leads → contactados → demos → cerrados)
- Leads por zona geográfica
- Pipeline por temperatura (frío/tibio/caliente)
- Tabla de prospectos activos con status visual
- Llamadas por semana con tendencia

---

### 📊 Reporte Ejecutivo Mensual

> *"Mi jefe quiere un reporte de KPIs cada lunes"*

Copias los resultados de tu query SQL → Claude genera:
- Dashboard automático con los KPIs detectados
- Gráficos apropiados según el tipo de dato
- Tabla de detalle con los datos completos
- HTML que envías por WhatsApp o email

---

## Cómo funciona

### Paso 1 — Tú subes tu data

```
Tú: Analiza estos datos y crea un dashboard para mi celular

nombre,ventas,mes,region
Producto A,12400,Enero,Norte
Producto B,9800,Enero,Sur
Producto A,15200,Febrero,Norte
Producto B,11300,Febrero,Sur
Producto A,18100,Marzo,Norte
Producto B,13700,Marzo,Sur
```

### Paso 2 — Claude analiza y perfila

```
📊 DataPocket — Data Profile

Summary:
- Rows: 6
- Columns: 4
- Types detected: nombre(VARCHAR), ventas(BIGINT), mes(VARCHAR), region(VARCHAR)
- Nulls: 0%

SQL generado: ✅ CREATE TABLE + INSERT listo para PostgreSQL
```

### Paso 3 — Claude transforma si es necesario

```
🔄 Operaciones aplicadas:
- Eliminados duplicados
- Agregado por mes (SUM ventas)
- Ordenado cronológicamente
- Código Python reproducible generado ✅
```

### Paso 4 — Claude genera tu dashboard

Te entrega un archivo HTML autocontenido:
- Optimizado para pantallas de 320px-480px
- Charts interactivos con Chart.js
- Dark mode por defecto
- Bottom bar estilo app nativa

### Paso 5 — Tú lo abres en tu celular

Opciones para acceder:
1. **GitHub Pages** (gratis) → URL permanente
2. **WhatsApp** → Te envías el archivo HTML
3. **Google Drive** → Lo subes y abres en Chrome mobile
4. **Home Screen** → Agrégalo como "app" en tu iPhone/Android

---

## Setup en 3 minutos

### 1. Instala

```bash
pip install mcp pydantic httpx
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
 Crea un dashboard mobile-first para consultarlo en mi celular."
```

Listo. Sin más.

---

## Stack técnico (todo gratis)

```
┌──────────────┐     ┌────────────────┐     ┌──────────────────┐
│  Tu data     │────▶│  Claude +      │────▶│  Dashboard HTML  │
│  CSV / JSON  │     │  DataPocket    │     │  Mobile-First    │
│  SQL Results │     │  MCP           │     │  Chart.js        │
└──────────────┘     └───────┬────────┘     └──────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              ┌─────▼─────┐   ┌──────▼──────┐
              │ PostgreSQL │   │  Power BI   │
              │ (gratuito) │   │  Desktop    │
              │            │   │  (gratuito) │
              └────────────┘   └─────────────┘
```

| Componente | Costo | Alternativa paga |
|-----------|-------|-----------------|
| Python | $0 | — |
| PostgreSQL | $0 | SQL Server ($15K+/año) |
| Power BI Desktop | $0 | Tableau ($75/user/mes) |
| DataPocket MCP | $0 | Looker ($5,000/mes) |
| Chart.js | $0 | Highcharts ($590/año) |
| GitHub Pages hosting | $0 | Hosting ($20-100/mes) |
| **Total** | **$0** | **$6,000+/año** |

---

## Tools incluidos

| Tool | Qué hace |
|------|----------|
| `datapocket_ingest_data` | Perfila tu data, infiere tipos, genera SQL para PostgreSQL |
| `datapocket_transform` | Limpia, filtra, agrega datos + genera código Python reproducible |
| `datapocket_generate_dashboard` | Crea dashboards HTML mobile-first con KPIs, charts y tablas |
| `datapocket_query_to_dashboard` | Convierte resultados SQL en dashboards auto-visualizados |
| `datapocket_powerbi_setup` | Genera conexión Power BI (código M + medidas DAX) |

---

## Demo en vivo

Abre este archivo en tu celular para ver un ejemplo real:

👉 **[`dashboards/demo_veterinarias.html`](./dashboards/demo_veterinarias.html)**

Incluye: KPIs, funnel de ventas, donut por zona, líneas de tendencia, pipeline por temperatura, y tabla de prospectos.

---

## Estructura del repo

```
datapocket-mcp/
├── README.md                          ← Estás aquí
├── requirements.txt                   ← pip install
├── src/
│   └── datapocket_mcp.py             ← MCP Server (5 tools)
├── dashboards/
│   └── demo_veterinarias.html        ← Demo funcional mobile-first
├── assets/
│   └── hero-mockup.svg               ← Mockups de resultado
└── examples/
    ├── ventas_ejemplo.csv            ← CSV de prueba
    └── finanzas_ejemplo.csv          ← CSV financiero de prueba
```

---

## FAQ

**¿Necesito saber programar?**
No. Tú hablas con Claude en español. Claude hace todo.

**¿Necesito instalar PostgreSQL?**
Solo si quieres guardar los datos permanentemente. Para dashboards rápidos, solo necesitas pegar tu CSV.

**¿Puedo compartir el dashboard?**
Sí. Es un archivo HTML. Lo envías por WhatsApp, email, o lo subes a GitHub Pages gratis.

**¿Funciona en iPhone y Android?**
Sí. Es HTML responsive optimizado para pantallas de 320px a 480px.

**¿Puedo conectar Power BI?**
Sí. El tool `datapocket_powerbi_setup` genera todo el código M y DAX listo para copiar y pegar.

---

<div align="center">

**Hecho por [DailyDuty](https://github.com/RodrigoInfante48) — Instituto para el Desarrollo Diario**

*De datos crudos a decisiones inteligentes. En tu celular. Gratis.*

</div>
