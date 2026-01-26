# Verificar y Habilitar Workflow Schedule

## 🔍 Problema Detectado

El workflow **NO se está ejecutando automáticamente**. Solo hay ejecuciones manuales.

## ✅ Verificación en GitHub Web

**IMPORTANTE:** Debes verificar manualmente en GitHub:

1. Ve a: **https://github.com/cuxaro/incidencias-adif-web/actions**
2. Click en **"Actualizar Datos Cada 5 Minutos"**
3. **Busca un botón o mensaje que diga "Enable workflow"** o "Workflow disabled"
4. Si está deshabilitado, **click en "Enable workflow"**

## 🔧 Verificar desde CLI

```bash
# Ver estado del workflow
gh api repos/cuxaro/incidencias-adif-web/actions/workflows/actualizar_datos.yml
```

Busca el campo `state` - debe ser `active`, no `disabled`.

## ⚠️ Limitaciones Conocidas

GitHub Actions tiene problemas conocidos con schedules muy frecuentes:
- Pueden tener **delays de hasta 30 minutos**
- Pueden ejecutarse **2-4 veces por hora** en lugar de 12 veces
- **No son 100% confiables** para cada 5 minutos

## 💡 Soluciones

### Opción 1: Verificar que Está Habilitado

Primero, asegúrate de que el workflow está habilitado en GitHub web.

### Opción 2: Aumentar Intervalo (Más Confiable)

Si el problema persiste, cambiar a 10 minutos es más confiable:

```yaml
schedule:
  - cron: '*/10 * * * *'  # Cada 10 minutos
```

### Opción 3: Usar Servicio Externo

Si necesitas precisión exacta cada 5 minutos, usar un servicio externo que haga ping a GitHub.

## 🧪 Probar Manualmente

Para verificar que el workflow funciona:

```bash
gh workflow run "Actualizar Datos Cada 5 Minutos" --repo cuxaro/incidencias-adif-web
```

Si funciona manualmente pero no automáticamente, el problema es con el schedule.
