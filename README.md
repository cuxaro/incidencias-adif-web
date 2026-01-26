# Web Estática - Incidencias ADIF

Web estática optimizada para GitHub Pages que muestra las incidencias ferroviarias activas de ADIF.

## 🚀 Despliegue en GitHub Pages

Esta web se despliega automáticamente en GitHub Pages usando GitHub Actions.

### Configuración inicial

1. **Crear repositorio en GitHub** (puede ser privado o público)

2. **Inicializar git localmente**:
```bash
cd web
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

3. **Habilitar GitHub Pages**:
   - Ve a Settings > Pages en tu repositorio
   - Source: GitHub Actions
   - El workflow `.github/workflows/deploy.yml` se ejecutará automáticamente

### Actualización de datos

El workflow de GitHub Actions se ejecuta automáticamente:
- Cada vez que haces push a `main`
- Puedes ejecutarlo manualmente desde la pestaña "Actions"

**Nota**: Para que el workflow funcione, necesitas tener el archivo `historico_incidencias.json` disponible. Tienes dos opciones:

1. **Opción A**: Subir `historico_incidencias.json` al repositorio (recomendado si es pequeño)
2. **Opción B**: Modificar el workflow para descargarlo desde otro lugar o usar secrets

## 📁 Estructura

```
web/
├── index.html          # Página principal
├── style.css          # Estilos CSS optimizados
├── script.js          # JavaScript mínimo para filtros
├── incidencias.json   # Datos generados (se crea automáticamente)
├── .github/
│   └── workflows/
│       └── deploy.yml  # Workflow de GitHub Actions
└── README.md          # Este archivo
```

## 🔧 Desarrollo local

Para probar localmente:

### Opción 1: Con historico_incidencias.json en web/

1. Copia `historico_incidencias.json` desde el proyecto raíz a `web/`:
```bash
cp ../historico_incidencias.json .
```

2. Genera `incidencias.json`:
```bash
python generate.py
```

3. Abre `index.html` en tu navegador o usa un servidor local:
```bash
python -m http.server 8000
# Abre http://localhost:8000
```

### Opción 2: Desde el proyecto raíz

```bash
cd ..
python generar_web.py
cd web
python -m http.server 8000
```

## 📊 Características

- ✅ Optimizado para PageSpeed 100/100
- ✅ Sin dependencias externas
- ✅ Búsqueda y filtros en tiempo real
- ✅ Diseño responsive
- ✅ Despliegue automático con GitHub Actions
