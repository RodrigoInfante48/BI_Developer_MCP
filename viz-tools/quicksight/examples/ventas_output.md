# ☁️ DataPocket — Amazon QuickSight Setup

## Fuente: `S3` · Región: `us-east-1` · Cuenta: `123456789012`
- **Tablas**: `ventas`
- **Base de datos**: `datapocket` · **Schema**: `public`
- **Columna de medida**: `ventas_usd` · **Columna de fecha**: `mes`

> _Generado con `datapocket_quicksight_setup` usando `examples/ventas_ejemplo.csv`_

---

## 1. Manifest JSON — S3 File Locations
Guarda como `s3://my-datapocket-ventas/manifest.json`:

```json
{
  "fileLocations": [
    {
      "URIPrefixes": [
        "s3://my-datapocket-ventas/ventas/"
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

---

## 2. Dataset Configuration JSON (CreateDataSet API)
Guarda como `dataset-ventas.json` para usar con AWS CLI:

```json
{
  "AwsAccountId": "123456789012",
  "DataSetId": "dataset-ventas",
  "Name": "ventas",
  "ImportMode": "SPICE",
  "PhysicalTableMap": {
    "ventas-physical": {
      "S3Source": {
        "DataSourceArn": "arn:aws:quicksight:us-east-1:123456789012:datasource/s3-datapocket",
        "UploadSettings": {
          "Format": "CSV",
          "StartFromRow": 1,
          "ContainsHeader": true,
          "Delimiter": ","
        },
        "InputColumns": [
          {"Name": "id",          "Type": "INTEGER"},
          {"Name": "ventas_usd",  "Type": "DECIMAL"},
          {"Name": "nombre",      "Type": "STRING"},
          {"Name": "mes",         "Type": "DATETIME"}
        ]
      }
    }
  }
}
```

> **Nota de columnas reales del dataset `ventas_ejemplo.csv`:**
> `producto` (STRING), `ventas_usd` (DECIMAL), `unidades` (INTEGER),
> `mes` (STRING/DATETIME), `region` (STRING), `vendedor` (STRING).
> Ajusta `InputColumns` con todos los campos al crear el DataSet en la consola.

---

## 3. Calculated Fields — Sintaxis QuickSight Nativa

### Calculated Field 1 — % del Total de Ventas
```
sumOver({ventas_usd}, [{ventas}], PRE_AGG) / sumOver({ventas_usd}, [], PRE_AGG)
```
**Uso**: Visual tipo KPI o tabla → muestra qué % aporta cada producto/región al total.

### Calculated Field 2 — YoY Growth (Year-over-Year)
```
(periodToDateSum({ventas_usd}, now(), YEAR) - periodToDateSum({ventas_usd}, addDateTime(-1, 'YYYY', now()), YEAR)) / periodToDateSum({ventas_usd}, addDateTime(-1, 'YYYY', now()), YEAR)
```
**Uso**: Visual tipo Line Chart con filtro de año → comparar crecimiento anual.

### Calculated Field 3 — Clasificación de Ventas
```
ifelse({ventas_usd} >= 10000, 'Alto', {ventas_usd} >= 5000, 'Medio', 'Bajo')
```
**Resultado esperado con los datos de ejemplo**:
| producto | ventas_usd | clasificacion |
|---|---|---|
| Zapatos Runner | 5600 | Medio |
| Camiseta Premium | 4200 | Bajo |
| Jeans Classic | 3800 | Bajo |

### Calculated Field 4 — Días desde la Venta
```
dateDiff({mes}, now(), 'DD')
```
**Uso**: Identifica registros más antiguos para priorizar actualización de datos.

### Calculated Field 5 — Ranking por Ventas
```
rank([{ventas_usd} DESC], [], PRE_AGG)
```
**Resultado esperado**: Zapatos Runner → Rank 1, Camiseta Premium → Rank 2, etc.

---

## 4. IAM Policy — Mínimo Privilegio para QuickSight (S3)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "QuickSightS3Read",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-datapocket-ventas",
        "arn:aws:s3:::my-datapocket-ventas/*"
      ]
    }
  ]
}
```

> Adjunta esta policy al IAM role de QuickSight:
> **IAM → Roles → aws-quicksight-service-role-v0 → Add permissions → Create inline policy**

---

## 5. AWS CLI Commands

```bash
# 1. Subir el manifest al bucket S3
aws s3 cp manifest.json s3://my-datapocket-ventas/manifest.json

# 2. Crear el DataSource S3
aws quicksight create-data-source \
  --aws-account-id 123456789012 \
  --data-source-id s3-datapocket \
  --name "datapocket (S3)" \
  --type S3 \
  --region us-east-1 \
  --data-source-parameters '{
    "S3Parameters": {
      "ManifestFileLocation": {
        "Bucket": "my-datapocket-ventas",
        "Key": "manifest.json"
      }
    }
  }'

# 3. Crear el DataSet (SPICE)
aws quicksight create-data-set \
  --aws-account-id 123456789012 \
  --region us-east-1 \
  --cli-input-json file://dataset-ventas.json

# 4. Verificar estado de ingesta SPICE
aws quicksight describe-ingestion \
  --aws-account-id 123456789012 \
  --data-set-id dataset-ventas \
  --ingestion-id initial-ingestion \
  --region us-east-1

# 5. Listar análisis disponibles
aws quicksight list-analyses \
  --aws-account-id 123456789012 \
  --region us-east-1
```

---

## 6. Instrucciones Paso a Paso (Consola AWS)

### Paso 1 — Requisitos previos
1. Cuenta AWS activa con QuickSight habilitado (Standard o Enterprise)
2. IAM policy aplicada (ver sección anterior)
3. CSV subido a S3: `aws s3 cp ventas_ejemplo.csv s3://my-datapocket-ventas/ventas/`
4. `manifest.json` subido al bucket raíz

### Paso 2 — Crear el DataSource en la consola
1. Ve a **QuickSight** → ícono de usuario (esquina superior derecha) → **Manage QuickSight**
2. Selecciona **Datasets** → **New dataset**
3. Elige conector: **S3**
4. Rellena:
   - **Data source name**: `datapocket-s3`
   - **Upload a manifest file**: selecciona **URL** → ingresa la URL del manifest
     `https://my-datapocket-ventas.s3.amazonaws.com/manifest.json`
5. Haz clic en **Connect** → luego **Create data source**

### Paso 3 — Crear el DataSet
1. En el DataSource creado → **Create dataset**
2. Elige **Import to SPICE for quicker analytics**
3. En **Edit/Preview data** revisa los tipos de columnas:
   - `ventas_usd` → `Decimal` ✅
   - `unidades` → `Integer` ✅
   - `mes` → cambia a `Date` si QuickSight no lo detecta automáticamente
4. **Save & publish** → nombre: `ventas-dataset`

### Paso 4 — Agregar Calculated Fields
1. En el dataset → **Add calculated field**
2. **Field name**: `pct_total_ventas`
   **Formula**: `sumOver({ventas_usd}, [{ventas}], PRE_AGG) / sumOver({ventas_usd}, [], PRE_AGG)`
3. Repite para los otros 4 campos calculados de la sección anterior
4. **Save**

### Paso 5 — Crear el Analysis
1. Dataset `ventas-dataset` → **Create analysis**
2. Agrega un **KPI visual**: métrica = `ventas_usd` (Sum), comparación = `pct_total_ventas`
3. Agrega un **Bar Chart**: eje X = `producto`, valor = `ventas_usd` (Sum)
4. Agrega un **Line Chart**: eje X = `mes`, valor = `ventas_usd` (Sum)
5. Filtra por `region` con un **Filter control**

### Paso 6 — Publicar como Dashboard
1. Analysis → **Share** → **Publish dashboard**
2. Nombre: `Ventas Dashboard - DataPocket`
3. Permisos: agrega Readers por email o grupo IAM
4. Copia el link y comparte con stakeholders

---

## 7. Costos — QuickSight Reader vs Author vs Enterprise

| Plan | Precio | Características | Ideal para |
| --- | --- | --- | --- |
| **Reader** | **$0.30/sesión** (máx $5/mes) | Solo consumo de dashboards publicados | Stakeholders, directivos |
| **Author** | **$18/usuario/mes** | Crear datasets, análisis y dashboards | Analistas de datos |
| **Author Pro** | **$28/usuario/mes** | Todo Author + Paginated Reports, forecasting avanzado | Reportes financieros |
| **Enterprise** | **desde $250/mes** (mín. 4 usuarios) | ML Insights, Q&A en lenguaje natural, row-level security | Equipos BI grandes |
| **Enterprise + Q** | **+$250/mes** | QuickSight Q (NLQ) habilitado para todos los readers | Self-service analytics |

> 💡 **Stack mínimo recomendado para este ejemplo**:
> 1 Author ($18/mes) + hasta 16 sesiones de Reader = **~$23/mes total**.
>
> 🎯 **Comparativa con alternativas**:
> - Tableau Cloud: $75/usuario/mes
> - Power BI Pro: $10/usuario/mes (solo Windows-native, limitado fuera de Azure)
> - Looker: $3,000+/mes
> - QuickSight: el más económico del ecosistema enterprise para equipos pequeños en AWS.

---

## Dataset de Ejemplo — ventas_ejemplo.csv

| producto | ventas_usd | unidades | mes | region | vendedor |
|---|---|---|---|---|---|
| Camiseta Premium | 4,200 | 140 | Enero | Norte | Carlos |
| Jeans Classic | 3,800 | 95 | Enero | Norte | Carlos |
| Zapatos Runner | 5,600 | 80 | Enero | Sur | María |
| Gorra Urban | 1,200 | 200 | Enero | Sur | María |
| ... | ... | ... | ... | ... | ... |

**Total registros**: 25 · **Rango**: Enero–Mayo 2026 · **Fuente**: `examples/ventas_ejemplo.csv`
