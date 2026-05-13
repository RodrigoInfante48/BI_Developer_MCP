# Amazon QuickSight — AWS Ecosystem

**Tool MCP:** `datapocket_quicksight_setup`  
**Ecosistema:** Amazon Web Services (AWS)  
**Costo base:** Reader $0.30/sesión (máx $5/mes) · Author $18/usuario/mes · Enterprise desde $250/mes  
**Estado:** 🔜 Próxima implementación

---

## ¿Qué generará este tool?

Todo lo necesario para conectar Amazon QuickSight a tus datos en PostgreSQL, S3, Athena o Redshift.

### 1. Manifest JSON (para fuentes S3)

```json
{
  "fileLocations": [
    {
      "URIs": [
        "s3://mi-bucket/data/ventas/ventas_2025.csv"
      ]
    }
  ],
  "globalUploadSettings": {
    "format": "CSV",
    "delimiter": ",",
    "containsHeader": "true"
  }
}
```

### 2. Dataset Configuration JSON (API QuickSight)

Listo para usar con `aws quicksight create-data-set`:

```json
{
  "AwsAccountId": "123456789012",
  "DataSetId": "ventas-dataset",
  "Name": "Ventas Dataset",
  "ImportMode": "SPICE",
  "PhysicalTableMap": {
    "ventas-table": {
      "RelationalTable": {
        "DataSourceArn": "arn:aws:quicksight:us-east-1:123456789012:datasource/postgres-source",
        "Schema": "public",
        "Name": "ventas",
        "InputColumns": [
          { "Name": "id", "Type": "INTEGER" },
          { "Name": "revenue", "Type": "DECIMAL" },
          { "Name": "fecha", "Type": "DATETIME" },
          { "Name": "categoria", "Type": "STRING" }
        ]
      }
    }
  }
}
```

### 3. Calculated Fields — Sintaxis QuickSight

```
// % del total por categoría
sumOver(revenue, [categoria], PRE_AGG) / sumOver(revenue, [], PRE_AGG)

// YoY Growth
(revenue - periodToDateSum(revenue, fecha, YEAR, -1)) /
  periodToDateSum(revenue, fecha, YEAR, -1)

// Clasificación condicional
ifelse(revenue > 10000, "Alto", revenue > 5000, "Medio", "Bajo")

// Diferencia en días
dateDiff(fecha_inicio, fecha_fin, "DD")
```

### 4. IAM Policy mínima

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::mi-bucket",
        "arn:aws:s3:::mi-bucket/*"
      ]
    }
  ]
}
```

---

## Prerrequisitos

| Componente | Costo | Notas |
|---|---|---|
| AWS Account | Gratis | Se requiere para cualquier uso |
| QuickSight Author | $18/usuario/mes | Para crear dashboards |
| QuickSight Reader | $0.30/sesión | Para consumir dashboards |
| SPICE capacity | 1 GB gratis | $0.25/GB adicional/mes |

---

## Fuentes de datos soportadas

| Fuente | Caso de uso |
|---|---|
| **PostgreSQL** | RDBMS local/RDS |
| **Amazon S3** | CSV/Parquet/JSON en S3 |
| **Amazon Athena** | Consultas sobre S3 (serverless) |
| **Amazon Redshift** | Data Warehouse empresarial |
| **MySQL / Aurora** | RDBMS AWS-managed |

---

## Diferencias clave vs Power BI

| Aspecto | Power BI | QuickSight |
|---|---|---|
| Modelo | DAX semántico | SQL + cálculos en columnas |
| ETL | Power Query M | AWS Glue / Athena / SQL propio |
| Integración cloud | Azure/Microsoft 365 | AWS nativo (S3, Redshift, Glue) |
| Pago | Por usuario | Por sesión (ideal para muchos viewers) |
| Fortaleza | Self-service Microsoft | Escala AWS, costo por consumo |

---

## Casos de uso ideales

- **Stacks AWS nativos** con datos en S3, Redshift o Athena
- **Muchos consumidores, pocos autores** — el modelo Reader $0.30/sesión es muy económico
- **Embedded analytics** — QuickSight puede embedarse en apps via SDK
- **Serverless BI** — análisis sobre datos en S3 sin base de datos

---

## Archivos de ejemplo

Ver carpeta `examples/` para outputs de muestra una vez implementado el tool.
