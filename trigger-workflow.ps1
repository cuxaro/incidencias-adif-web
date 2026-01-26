# Script para Ejecutar Workflow Externamente

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
    Write-Host "Response: $($response | ConvertTo-Json)"
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Detalles: $responseBody" -ForegroundColor Yellow
    }
}
