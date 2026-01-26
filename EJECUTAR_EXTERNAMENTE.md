# Ejecutar Workflow Externamente

## 🔗 Métodos para Ejecutar el Workflow desde Fuera de GitHub

### Método 1: Usar GitHub API (Recomendado)

Puedes usar la API de GitHub para ejecutar el workflow usando `workflow_dispatch`.

#### Con curl:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer TU_PERSONAL_ACCESS_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches \
  -d '{"ref":"main"}'
```

#### Con PowerShell:

```powershell
$token = "TU_PERSONAL_ACCESS_TOKEN"
$headers = @{
    "Accept" = "application/vnd.github+json"
    "Authorization" = "Bearer $token"
    "X-GitHub-Api-Version" = "2022-11-28"
}
$body = @{
    ref = "main"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches" -Method Post -Headers $headers -Body $body
```

#### Con Python:

```python
import requests

token = "TU_PERSONAL_ACCESS_TOKEN"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}
data = {"ref": "main"}

response = requests.post(
    "https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches",
    headers=headers,
    json=data
)
print(response.status_code)
```

### Método 2: Usar Servicio Externo (Más Simple)

#### Opción A: Cron-job.org (Gratis)

1. Ve a: https://cron-job.org/
2. Crea cuenta gratuita
3. Crea nuevo cron job:
   - **URL:** `https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches`
   - **Método:** POST
   - **Headers:**
     - `Authorization: Bearer TU_PAT`
     - `Accept: application/vnd.github+json`
     - `X-GitHub-Api-Version: 2022-11-28`
   - **Body (JSON):** `{"ref":"main"}`
   - **Frecuencia:** Cada 5 o 10 minutos

#### Opción B: UptimeRobot (Gratis)

UptimeRobot puede hacer ping a una URL, pero necesitarías crear un endpoint que active el workflow.

#### Opción C: GitHub CLI desde Servidor

Si tienes un servidor, puedes usar `gh` CLI:

```bash
gh workflow run "Actualizar Datos Cada 10 Minutos" --repo cuxaro/incidencias-adif-web
```

Y programarlo con cron del sistema.

## 🔐 Crear Personal Access Token (PAT)

Para usar la API, necesitas un PAT:

1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Configura:
   - **Note:** `Workflow Trigger Token`
   - **Scopes:** ✅ `repo` (acceso completo a repositorios)
   - **Expiration:** Elige duración
4. Click "Generate token"
5. **Copia el token** (solo se muestra una vez)

## 📝 Ejemplo Completo con Cron-job.org

### Configuración:

1. **URL:**
```
https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches
```

2. **Método:** POST

3. **Headers:**
```
Authorization: Bearer ghp_TU_TOKEN_AQUI
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
Content-Type: application/json
```

4. **Body:**
```json
{
  "ref": "main"
}
```

5. **Frecuencia:** Cada 5 minutos (o la que prefieras)

## ✅ Ventajas de Ejecución Externa

- ✅ **Más confiable** - No depende de delays de GitHub Actions
- ✅ **Más preciso** - Se ejecuta exactamente cuando quieres
- ✅ **Más control** - Puedes elegir el servicio y frecuencia

## 🔧 Script PowerShell para Ejecutar Localmente

Guarda esto como `trigger-workflow.ps1`:

```powershell
# trigger-workflow.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$headers = @{
    "Accept" = "application/vnd.github+json"
    "Authorization" = "Bearer $Token"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$body = @{
    ref = "main"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches" -Method Post -Headers $headers -Body $body
    Write-Host "✅ Workflow ejecutado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

**Uso:**
```powershell
.\trigger-workflow.ps1 -Token "TU_PAT"
```
