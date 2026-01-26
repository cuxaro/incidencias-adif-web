# URLs Útiles del Repositorio Web

## 🔗 URLs Principales

### GitHub Actions (Workflows y Ejecuciones)
```
https://github.com/cuxaro/incidencias-adif-web/actions
```
**Qué verás:**
- Lista de todos los workflows
- Historial de ejecuciones
- Estado de cada ejecución (success/failure)
- Logs de cada ejecución

### Workflow Específico: Actualizar Datos
```
https://github.com/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml
```
**Qué verás:**
- Solo ejecuciones del workflow "Actualizar Datos Cada 5 Minutos"
- Historial completo
- Botón "Run workflow" para ejecución manual

### GitHub Pages (Web Publicada)
```
https://cuxaro.github.io/incidencias-adif-web/
```
**Qué verás:**
- La web pública con las incidencias
- Datos actualizados automáticamente

### Settings del Repositorio
```
https://github.com/cuxaro/incidencias-adif-web/settings
```
**Qué verás:**
- Configuración del repositorio
- Secrets (Settings > Secrets and variables > Actions)
- Pages (Settings > Pages)

### Commits (Historial de Cambios)
```
https://github.com/cuxaro/incidencias-adif-web/commits/main
```
**Qué verás:**
- Historial de commits
- Commits automáticos del workflow (mensajes como "Auto-update: ...")

## 🔍 Cómo Verificar el Schedule

1. **Ve a:** `https://github.com/cuxaro/incidencias-adif-web/actions`
2. **Click en:** "Actualizar Datos Cada 5 Minutos"
3. **Verifica:**
   - Que aparezcan ejecuciones con evento **"schedule"** (no solo "workflow_dispatch")
   - Que se ejecuten aproximadamente cada 5 minutos
   - Que el estado sea "completed" y "success"

## 📊 Qué Buscar

### Ejecuciones Automáticas:
- **Event:** `schedule` (no `workflow_dispatch`)
- **Frecuencia:** Aproximadamente cada 5 minutos
- **Estado:** `completed` con `success`

### Si Solo Ves Ejecuciones Manuales:
- El schedule no está funcionando
- Puede ser delay de GitHub Actions
- O problema de configuración
