# Verificar Por Qué No Se Ejecuta el Schedule

## 🔍 Diagnóstico

El workflow **DEBE** ejecutarse automáticamente cada 5 minutos. Si no lo hace, puede ser por:

### Posibles Problemas:

1. **Workflow deshabilitado** - Verificar en GitHub web
2. **Delay en primera ejecución** - Puede tardar hasta 10-15 minutos
3. **Problemas de confiabilidad** - GitHub Actions puede tener delays
4. **Workflow no está en la rama correcta** - Debe estar en `main`

## ✅ Verificaciones Necesarias

### 1. Verificar que el Workflow Está Habilitado

Ve a: `https://github.com/cuxaro/incidencias-adif-web/actions`

1. Click en "Actualizar Datos Cada 5 Minutos"
2. Verifica que NO dice "Workflow disabled"
3. Si está deshabilitado, click en "Enable workflow"

### 2. Verificar el Cron en el Archivo

El archivo debe tener:
```yaml
on:
  schedule:
    - cron: '*/5 * * * *'
```

### 3. Verificar que Está en la Rama Main

```bash
# Verificar que el workflow está en main
gh workflow view "Actualizar Datos Cada 5 Minutos" --repo cuxaro/incidencias-adif-web --yaml
```

## 🧪 Probar Ahora

### Ejecutar Manualmente para Verificar que Funciona:

```bash
gh workflow run "Actualizar Datos Cada 5 Minutos" --repo cuxaro/incidencias-adif-web
```

Si funciona manualmente pero no automáticamente, el problema es con el schedule.

## ⚠️ Limitaciones Conocidas de GitHub Actions

Según la documentación:
- Los schedules pueden tener **delays de hasta 30 minutos**
- Pueden ejecutarse **2-4 veces por hora** en lugar de 12 veces (cada 5 min)
- No son 100% confiables para intervalos muy frecuentes

## 🔧 Soluciones Alternativas

Si el schedule no funciona bien, podemos:

1. **Aumentar el intervalo** a 10 o 15 minutos (más confiable)
2. **Usar un servicio externo** que haga ping a GitHub cada 5 minutos
3. **Aceptar los delays** como limitación de GitHub Actions

## 📝 Próximos Pasos

1. **Verifica en GitHub web** si el workflow está habilitado
2. **Espera hasta las 15:40** y verifica si aparece ejecución automática
3. **Si no aparece**, puede ser un problema de GitHub Actions con schedules frecuentes
