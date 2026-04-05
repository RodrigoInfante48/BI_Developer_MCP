# BI Developer — Reglas de Comportamiento Obligatorias

Este archivo define el comportamiento estricto que Claude debe seguir en CADA sesión de trabajo con dashboards y visualización de datos.

---

## FLUJO DE TRABAJO: DOS FASES OBLIGATORIAS

### FASE 1 — LEER Y CONFIRMAR LA DATA (SIEMPRE PRIMERO)

Antes de tocar cualquier archivo HTML, CSS o JS:

1. **Leer el archivo de datos** indicado por el usuario (CSV, JSON, Excel, etc.)
2. **Responder con un resumen estructurado** que incluya:
   - Nombre del archivo leído
   - Tipo de datos que contiene
   - Lista de campos / columnas encontrados
   - Cantidad de registros
   - Rango de fechas (si aplica)
   - 3–5 métricas o insights clave encontrados en los datos
   - Confirmación explícita: _"Solo usaré estos datos. No agregaré información externa."_
3. **Esperar confirmación del usuario** ("ok", "procede", "sí", etc.) antes de continuar.

> **PROHIBIDO** avanzar a la Fase 2 sin confirmación explícita del usuario.

---

### FASE 2 — CONSTRUIR EL DASHBOARD (SOLO TRAS CONFIRMACIÓN)

#### REGLAS DE DATOS (irrompibles)

- Usar **ÚNICAMENTE** los datos del archivo proporcionado. Cero inventos.
- Si un campo no existe en el archivo, **no mostrarlo**.
- Todos los números, etiquetas y categorías deben coincidir **exactamente** con el archivo.
- Si los datos son insuficientes para un tipo de gráfico, usar otro tipo más simple.
- **Nunca** rellenar datos faltantes con suposiciones o promedios inventados.

#### DISEÑO — KanbanPro Style

- Fondo oscuro `#1e1e2f`, texto blanco, acentos neón verde `#39ff8e` y azul `#5bc8fc`
- Mobile-first: `viewport` meta tag, layout Flexbox columna única, `max-width: 520px`
- KPI cards al 100% de ancho, tipografía grande, `border-radius: 16px`
- **Chart.js** para gráficos (CDN). Barras horizontales para rankings. Altura máxima 300px por gráfico.
- Botones y elementos táctiles con `min-height: 44px`
- Todo en un **único archivo `index.html`** (CSS y JS embebidos)

#### ESTRUCTURA DEL DASHBOARD

1. **Header** — nombre real del negocio/dataset + fecha de los datos
2. **KPI cards** — métricas más importantes extraídas del archivo
3. **Gráfico principal** — el que mejor represente los datos encontrados
4. **Gráfico secundario** — comparativo, tendencia o ranking según lo disponible
5. **Tabla resumen** — datos detallados del archivo
6. **Footer** — fuente real del archivo

#### ENTREGABLE

- Reemplazar `index.html` en el repositorio
- Commit con mensaje descriptivo
- Push a la branch activa

---

## ANTI-ALUCINACIÓN: LO QUE NUNCA HACER

- No inventar registros, métricas o categorías que no estén en el archivo
- No agregar "datos de ejemplo" si el archivo ya tiene datos reales
- No usar datos de sesiones anteriores en una nueva sesión
- No asumir campos que no se han leído — siempre leer primero
- No avanzar a Fase 2 sin confirmación del usuario en Fase 1

---

## RECORDATORIO AUTOMÁTICO

Al inicio de cada tarea de dashboard, Claude debe indicar:

> "Voy a leer el archivo de datos primero. No construiré nada hasta confirmar los datos contigo."
