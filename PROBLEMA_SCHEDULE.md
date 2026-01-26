# Problema: Schedule No Se Ejecuta Automáticamente

## 🔍 Diagnóstico

El workflow **DEBE** ejecutarse cada 5 minutos automáticamente, pero parece que no lo está haciendo.

### Verificaciones Realizadas:

✅ Cron configurado correctamente: `*/5 * * * *`
✅ Repositorio es público
✅ Workflow existe en la rama main

### Posibles Causas:

1. **Workflow deshabilitado** - Verificar en GitHub web
2. **Delays de GitHub Actions** - Pueden ser de hasta 30 minutos
3. **Problemas conocidos** - GitHub Actions no es 100% confiable con schedules muy frecuentes

## ✅ Verificar en GitHub Web

**IMPORTANTE:** Ve a GitHub y verifica:

1. Abre: `https://github.com/cuxaro/incidencias-adif-web/actions`
2. Click en "Actualizar Datos Cada 5 Minutos"
3. **Verifica que NO dice "Workflow disabled"**
4. Si está deshabilitado, click en **"Enable workflow"**

## 🔧 Solución Temporal: Verificar Estado

Ejecuta esto para ver el estado actual:

```bash
# Ver últimas ejecuciones
gh run list --repo cuxaro/incidencias-adif-web --workflow "Actualizar Datos Cada 5 Minutos" --limit 10

# Ver detalles del workflow
gh workflow view "Actualizar Datos Cada 5 Minutos" --repo cuxaro/incidencias-adif-web
```

## ⚠️ Limitación Conocida de GitHub Actions

Según la documentación oficial y reportes de usuarios:
- Los schedules pueden tener **delays significativos**
- Pueden ejecutarse **2-4 veces por hora** en lugar de 12 veces (cada 5 min)
- **No son 100% confiables** para intervalos muy frecuentes

## 💡 Soluciones

### Opción 1: Aumentar Intervalo (Más Confiable)

Cambiar a 10 o 15 minutos es más confiable:

```yaml
schedule:
  - cron: '*/10 * * * *'  # Cada 10 minutos
```

### Opción 2: Usar Servicio Externo

Usar un servicio como:
- **UptimeRobot** (gratis) - Hace ping cada 5 minutos
- **Cron-job.org** (gratis) - Ejecuta webhook cada 5 minutos

### Opción 3: Aceptar los Delays

Es una limitación conocida de GitHub Actions. Los schedules funcionan, pero no son precisos.

## 🧪 Probar Ahora

Ejecuta manualmente para verificar que funciona:

```bash
gh workflow run "Actualizar Datos Cada 5 Minutos" --repo cuxaro/incidencias-adif-web
```

Si funciona manualmente pero no automáticamente, el problema es con el schedule de GitHub Actions.
