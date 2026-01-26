# Flujo Completo de Actualización

## 🔄 Proceso Automatizado

### 1. Trigger desde Cron-Job
- **Cron-job.org** llama cada 10 minutos a:
  ```
  POST https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches
  ```
- Esto dispara el workflow `Actualizar Datos Cada 10 Minutos` con evento `workflow_dispatch`

### 2. Ejecución del Script Python
El workflow ejecuta `actualizar_datos.py` que realiza:

#### Paso 1: Scraping de ADIF
- Conecta a `https://www.adif.es/viajeros/estado-de-la-red`
- Extrae todas las incidencias activas
- Guarda los textos raw

#### Paso 2: Actualizar `historico_incidencias.json`
- Carga el histórico existente
- Compara con nuevas incidencias (usando hash MD5)
- **Añade nuevas incidencias** al histórico
- **Actualiza** `ultima_vez_visto` para incidencias existentes
- Guarda `historico_incidencias.json`

#### Paso 3: Análisis con IA (solo nuevas)
- Para cada incidencia **sin análisis previo**:
  - Llama a Gemini 2.0 Flash
  - Extrae: red, línea, ubicación, estado, severidad, etc.
  - Guarda el análisis en `historico_incidencias.json`

#### Paso 4: Generar `incidencias.json` para la web
- Filtra solo incidencias **activas** (is_active=True o status=RED/YELLOW)
- **SIEMPRE actualiza** `generated_at` con la fecha/hora actual
- Ordena por severidad (mayor a menor)
- Guarda `incidencias.json`

### 3. Commit y Push
- El workflow hace commit de ambos archivos:
  - `incidencias.json` (siempre cambia por el timestamp)
  - `historico_incidencias.json` (si hay cambios)
- Push al repositorio

### 4. Deploy Automático
- Después del push, el workflow dispara automáticamente:
  - `Deploy to GitHub Pages`
- Esto actualiza la web pública con los nuevos datos

## ⚠️ Problema Resuelto

**Antes:** El `generated_at` no se actualizaba porque:
- Git no detectaba cambios si el contenido era idéntico
- El deploy no se ejecutaba automáticamente

**Ahora:**
- ✅ El script **siempre** actualiza `generated_at` con la fecha/hora actual
- ✅ El workflow **siempre** hace commit de `incidencias.json` (el timestamp cambia)
- ✅ El deploy se dispara **automáticamente** después de cada commit
- ✅ La web se actualiza con el nuevo timestamp

## 🔍 Verificar que Funciona

1. **Ver última ejecución:**
   ```bash
   gh run list --repo cuxaro/incidencias-adif-web --workflow "Actualizar Datos Cada 10 Minutos" --limit 1
   ```

2. **Ver timestamp en GitHub:**
   ```bash
   gh api repos/cuxaro/incidencias-adif-web/contents/incidencias.json | ConvertFrom-Json | ForEach-Object { $content = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_.content)) ; $json = $content | ConvertFrom-Json ; Write-Host "generated_at: $($json.generated_at)" }
   ```

3. **Ver en la web:**
   - Abre: https://cuxaro.github.io/incidencias-adif-web/
   - El timestamp debería actualizarse cada 10 minutos
