# Web Estática - Incidencias ADIF

Web estática optimizada para GitHub Pages que muestra las incidencias ferroviarias activas de ADIF.

## 🚀 Despliegue Automático

Esta web se despliega automáticamente en GitHub Pages. Los datos se actualizan cada 5 minutos mediante un workflow automatizado.

## 📊 Actualización de Datos

Los datos se actualizan automáticamente:
- **Cada 5 minutos** mediante el workflow "Actualizar Datos Cada 5 Minutos"
- El workflow ejecuta scraping, análisis con IA y genera `incidencias.json`
- GitHub Pages se actualiza automáticamente después de cada actualización

## 📁 Estructura

```
web/
├── index.html              # Página principal
├── style.css              # Estilos CSS optimizados
├── script.js             # JavaScript para filtros y búsqueda
├── incidencias.json      # Datos generados automáticamente (no editar)
├── historico_incidencias.json  # Base de datos completa (actualizada automáticamente)
├── actualizar_datos.py   # Script de actualización (ejecutado por workflow)
└── .github/
    └── workflows/
        ├── actualizar_datos.yml  # Workflow de actualización (cada 5 min)
        └── deploy.yml            # Workflow de despliegue en Pages
```

## 🔧 Desarrollo Local

Para probar localmente:

1. **Generar datos** (si no tienes `incidencias.json`):
```bash
# El script actualizar_datos.py necesita historico_incidencias.json
python actualizar_datos.py
```

2. **Servir la web**:
```bash
python -m http.server 8000
# Abre http://localhost:8000
```

## 📊 Características

- ✅ Optimizado para PageSpeed 100/100
- ✅ Sin dependencias externas
- ✅ Búsqueda y filtros en tiempo real
- ✅ Diseño responsive
- ✅ Actualización automática cada 5 minutos
- ✅ Despliegue automático con GitHub Actions

## 🔐 Configuración

### Secrets Requeridos

- `GEMINI_API_KEY` - API key de Google Gemini para análisis con IA

### Configurar Secret:

```bash
gh secret set GEMINI_API_KEY --repo cuxaro/incidencias-adif-web --body "TU_API_KEY"
```

## 📝 Notas

- `incidencias.json` se genera automáticamente, no editar manualmente
- El workflow se ejecuta cada 5 minutos automáticamente
- Los datos se actualizan sin intervención manual
