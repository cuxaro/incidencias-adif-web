# Problema: Schedule No Se Ejecuta + Verificar Actualización de Datos

## 🔍 Diagnóstico Actual

### Estado del JSON:
- ✅ **GitHub:** Actualizado a `2026-01-26 15:06:49`
- ✅ **Local:** Sincronizado después del pull
- ❌ **Schedule:** NO se ejecuta automáticamente

### Ejecuciones:
- ✅ Ejecuciones manuales funcionan correctamente
- ❌ **NO hay ejecuciones automáticas** (schedule)

## ⚠️ Problema Principal

El **schedule de GitHub Actions NO funciona**. Solo se ejecuta manualmente.

## ✅ Soluciones

### Opción 1: Usar Servicio Externo (Recomendado)

**Cron-job.org** - Ejecuta el workflow cada 10 minutos:

1. Ve a: https://cron-job.org/
2. Crea cuenta gratuita
3. Nuevo cron job:
   - **URL:** `https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches`
   - **Método:** POST
   - **Headers:**
     ```
     Authorization: Bearer TU_PAT
     Accept: application/vnd.github+json
     X-GitHub-Api-Version: 2022-11-28
     Content-Type: application/json
     ```
   - **Body:** `{"ref":"main"}`
   - **Frecuencia:** Cada 10 minutos

### Opción 2: Ejecutar Manualmente Periódicamente

Puedes ejecutar manualmente cuando quieras:

```bash
gh workflow run "Actualizar Datos Cada 10 Minutos" --repo cuxaro/incidencias-adif-web
```

### Opción 3: Script Local con Task Scheduler

Crear un script que se ejecute cada 10 minutos en Windows:

```powershell
# trigger-every-10min.ps1
$token = "TU_PAT"
$headers = @{
    "Accept" = "application/vnd.github+json"
    "Authorization" = "Bearer $token"
    "X-GitHub-Api-Version" = "2022-11-28"
}
$body = @{"ref"="main"} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml/dispatches" -Method Post -Headers $headers -Body $body
```

Y programarlo con Task Scheduler de Windows cada 10 minutos.

## 🔍 Verificar si los Datos Cambian

El workflow puede ejecutarse pero generar los mismos datos si:
- No hay nuevas incidencias en ADIF
- Las incidencias son las mismas

Para verificar:
1. Ejecuta manualmente
2. Compara `generated_at` antes y después
3. Si cambia la fecha pero los datos son iguales = funciona correctamente
