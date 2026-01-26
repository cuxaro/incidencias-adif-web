# Solución: Timestamp No Se Actualiza en la Web

## 🔍 Problema Identificado

El timestamp `generated_at` en la web no se actualiza aunque el workflow se ejecuta correctamente.

## ✅ Verificaciones Realizadas

1. ✅ **Workflow de actualización funciona:** Se ejecuta desde cron-job y genera nuevos JSONs
2. ✅ **Commits se hacen correctamente:** Los archivos se pushean al repositorio
3. ✅ **Deploy se ejecuta automáticamente:** El workflow `deploy.yml` se dispara en cada push

## 🎯 Posibles Causas

### 1. Caché del Navegador
El navegador puede estar cacheando el archivo `incidencias.json`.

**Solución:**
- Presiona `Ctrl + F5` para forzar recarga sin caché
- O abre la consola del navegador (F12) y marca "Disable cache"

### 2. Caché de GitHub Pages CDN
GitHub Pages puede tener caché en su CDN.

**Solución:**
- Espera 1-2 minutos después del deploy
- O añade un parámetro de versión al fetch en `script.js`

### 3. El JSON no cambia realmente
Aunque el timestamp cambia, Git puede no detectar cambios si el contenido es idéntico.

**Verificación:**
```bash
# Ver el contenido actual en GitHub
gh api repos/cuxaro/incidencias-adif-web/contents/incidencias.json | ConvertFrom-Json | ForEach-Object { $content = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_.content)) ; $json = $content | ConvertFrom-Json ; Write-Host "generated_at: $($json.generated_at)" }
```

## 🔧 Solución Recomendada: Añadir Cache Busting

Modificar `script.js` para añadir un parámetro de versión al fetch:

```javascript
// En lugar de:
const response = await fetch('incidencias.json');

// Usar:
const response = await fetch(`incidencias.json?v=${Date.now()}`);
```

Esto fuerza al navegador a descargar siempre la versión más reciente.

## 📋 Checklist de Verificación

- [ ] Verificar que el workflow de actualización se ejecuta cada 10 minutos
- [ ] Verificar que hace commit y push
- [ ] Verificar que el deploy se ejecuta después del push
- [ ] Verificar el timestamp en GitHub: `gh api repos/cuxaro/incidencias-adif-web/contents/incidencias.json`
- [ ] Limpiar caché del navegador (Ctrl+F5)
- [ ] Verificar en modo incógnito
