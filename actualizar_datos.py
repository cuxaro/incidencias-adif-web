"""
Script automatizado para extracción de datos y generación de incidencias.json
Este script se ejecuta periódicamente (cada 5 minutos) mediante GitHub Actions
en el repositorio web público para evitar límites de minutos en repos privados
"""
import time
import json
import os
import hashlib
import sys
from datetime import datetime
from pathlib import Path

# Imports para scraping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Imports para IA
from google import genai

# Configuración
ADIF_URL = "https://www.adif.es/viajeros/estado-de-la-red"
ARCHIVO_DB = "historico_incidencias.json"
ARCHIVO_WEB_JSON = "incidencias.json"

# Prompt para la IA
MI_PROMPT_MAESTRO = """
### ROL
Actúa como un experto Analista de Datos Ferroviarios de Adif/Renfe especializado en Sistemas de Información Geográfica (GIS). Tu objetivo es convertir notificaciones de incidencias en lenguaje natural en objetos JSON estructurados para su mapeo automático.

### ESQUEMA DE SALIDA (JSON ESTRICTO)
Debes devolver exclusivamente un objeto JSON con los siguientes campos:
- "id": El identificador único proporcionado (o null).
- "summary": Resumen muy breve (máx 60 caracteres).
- "description": Texto íntegro de la incidencia.
- "network": Categoría de red: [CERCANIAS_MADRID, CERCANIAS_VALENCIA, RODALIES_CATALUNYA, ALTA_VELOCIDAD, MEDIA_DISTANCIA, ANCHO_METRICO, OTROS].
- "line_affected": Identificador de la línea (ej: "C4", "R1", "R2 Sud").
- "location_type": Tipo de geometría GIS: ["STATION", "SEGMENT", "LINE", "AREA"].
- "nodes": Lista de nombres de estaciones CLAVE. 
    - Si es SEGMENT, extraer [Origen, Destino] del patrón "entre X e Y".
    - Normalizar nombres (ej: "Valencia Nord" -> "VALENCIA-ESTACIO DEL NORD").
- "status": ["RED" (Corte/Interrupción), "YELLOW" (Retrasos), "BLUE" (Obras/Plan alternativo), "GREEN" (Subsanada)].
- "cause_category": ["OBRAS", "ACCIDENTE", "METEO", "INFRAESTRUCTURA", "OTROS"].
- "severity_level": Escala 1 a 5 (1: Informativo, 5: Interrupción total red crítica como AV).
- "start_date": Fecha en formato ISO (YYYY-MM-DD). Si dice "desde hoy", usar la fecha actual.
- "end_date": Fecha de finalización prevista (ISO) si aparece en el texto.
- "is_active": Boolean (true si la incidencia sigue vigente o es una obra futura).
- "transport_backup": Boolean (true si menciona "transbordo", "autobús" o "plan alternativo").

### REGLAS CRÍTICAS DE LÓGICA
1. **Detección de Red**: 
   - Líneas con prefijo "C" (ej: C3, C4, C9) -> CERCANIAS (identificar núcleo por ciudad mencionada).
   - Líneas con prefijo "R" (ej: R1, R2, R4) -> RODALIES_CATALUNYA.
2. **Geometría**:
   - Si el texto dice "entre [Estación A] y [Estación B]", el tipo es siempre SEGMENT.
   - Si menciona una línea completa sin tramos, es LINE.
3. **Severidad**:
   - Nivel 5: Accidentes en Alta Velocidad o cortes totales por DANA/Meteo.
   - Nivel 4: Cortes totales en líneas de Cercanías/Rodalies con transbordo.
   - Nivel 3: Obras programadas con afectación al servicio.
   - Nivel 2: Retrasos puntuales.
   - Nivel 1: Incidencias subsanadas o informativas.

### NOTA IMPORTANTE
No incluyas texto explicativo, solo el JSON. Si no puedes extraer un dato, usa null.
"""


def generar_hash(texto):
    """Crea un identificador único basado en el texto"""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()


def obtener_datos_adif():
    """Scraping de datos de ADIF"""
    print("👻 Iniciando navegador en modo silencioso (Headless)...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Para GitHub Actions, usar chromium del sistema si está disponible
    if os.path.exists('/usr/bin/chromium-browser'):
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        service = Service('/usr/bin/chromedriver')
    else:
        service = Service(ChromeDriverManager().install())

    driver = None
    try:
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        
        print(f"🌍 Conectando a {ADIF_URL}...")
        driver.get(ADIF_URL)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all(class_="estado-red-li")
        
        datos_encontrados = []
        for item in items:
            texto = item.get_text(" ", strip=True)
            if len(texto) > 10:
                datos_encontrados.append(texto)
                
        return datos_encontrados

    except Exception as e:
        print(f"❌ Error durante el scraping: {e}")
        return []
        
    finally:
        if driver:
            driver.quit()
            print("🔒 Navegador cerrado correctamente.")


def guardar_incidencias(lista_textos):
    """Guarda y deduplica incidencias en historico_incidencias.json"""
    # Cargar base de datos existente
    if os.path.exists(ARCHIVO_DB):
        try:
            with open(ARCHIVO_DB, 'r', encoding='utf-8') as f:
                db = json.load(f)
        except:
            db = {}
    else:
        db = {}

    nuevas = 0
    
    # Procesar datos
    for texto in lista_textos:
        id_hash = generar_hash(texto)
        
        # Si el ID no existe en nuestro JSON, es una incidencia nueva
        if id_hash not in db:
            db[id_hash] = {
                "id": id_hash,
                "descripcion": texto,
                "primera_vez_visto": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "estado": "Activa"
            }
            nuevas += 1
        else:
            # Si ya existe, actualizamos la fecha de última comprobación
            db[id_hash]["ultima_vez_visto"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar cambios
    if nuevas > 0 or not os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
            
    return nuevas, db


def analizar_con_ia(historico, api_key):
    """Analiza incidencias pendientes con IA"""
    if not api_key:
        print("⚠️ GEMINI_API_KEY no encontrada. Saltando análisis con IA.")
        return 0
        
    client = genai.Client(api_key=api_key)
    
    pendientes = [id_inc for id_inc, data in historico.items() if "analisis_ia" not in data]
    
    if not pendientes:
        print("☕ Todas las incidencias ya están analizadas.")
        return 0
    
    print(f"🧠 Analizando {len(pendientes)} incidencias con Gemini 2.0 Flash...")
    
    actualizaciones = 0
    for id_inc in pendientes:
        texto_incidencia = historico[id_inc]['descripcion']
        
        try:
            # Llamada a la IA
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"{MI_PROMPT_MAESTRO}\n\nIncidencia: {texto_incidencia}"
            )
            
            # Limpieza y carga de JSON
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            resultado_json = json.loads(raw_text)

            # Insertamos en el diccionario
            historico[id_inc]["analisis_ia"] = resultado_json
            actualizaciones += 1
            
            print(f"✅ Analizada: {id_inc[:8]} - {resultado_json.get('summary', '')[:50]}...")
            
        except Exception as e:
            print(f"❌ Error en {id_inc[:8]}: {e}")
            import traceback
            traceback.print_exc()

    # Guardar análisis
    if actualizaciones > 0:
        with open(ARCHIVO_DB, 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=4)
        print(f"💾 {actualizaciones} análisis guardados.")
    
    return actualizaciones


def generar_incidencias_web(historico):
    """Genera incidencias.json con solo las activas para la web"""
    incidencias_activas = []
    
    for id_inc, data in historico.items():
        if "analisis_ia" in data:
            analisis = data["analisis_ia"]
            # Considerar activa si is_active es True o si status es RED/YELLOW
            if analisis.get("is_active", False) or analisis.get("status") in ["RED", "YELLOW"]:
                incidencia = {
                    "id": id_inc,
                    "summary": analisis.get("summary", ""),
                    "description": analisis.get("description", data.get("descripcion", "")),
                    "descripcion_original": data.get("descripcion", ""),  # Descripción original de ADIF
                    "network": analisis.get("network", "OTROS"),
                    "line_affected": analisis.get("line_affected"),
                    "location_type": analisis.get("location_type", "LINE"),
                    "nodes": analisis.get("nodes", []),
                    "status": analisis.get("status", "BLUE"),
                    "cause_category": analisis.get("cause_category", "OTROS"),
                    "severity_level": analisis.get("severity_level", 1),
                    "start_date": analisis.get("start_date"),
                    "end_date": analisis.get("end_date"),
                    "transport_backup": analisis.get("transport_backup", False),
                    "primera_vez_visto": data.get("primera_vez_visto"),
                    "ultima_vez_visto": data.get("ultima_vez_visto")
                }
                incidencias_activas.append(incidencia)
    
    # Ordenar por severidad (mayor a menor) y luego por fecha
    incidencias_activas.sort(key=lambda x: (
        -x.get("severity_level", 0),
        x.get("start_date") or ""
    ))
    
    # Crear objeto final con metadata - SIEMPRE actualizar generated_at en UTC
    resultado = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(incidencias_activas),
        "incidencias": incidencias_activas
    }
    
    # Guardar SIEMPRE (incluso si los datos son iguales, el timestamp cambia)
    with open(ARCHIVO_WEB_JSON, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generado {ARCHIVO_WEB_JSON}")
    print(f"   - Total incidencias activas: {len(incidencias_activas)}")
    print(f"   - Timestamp: {resultado['generated_at']}")
    
    return resultado


def main():
    """Proceso principal automatizado"""
    print("=" * 60)
    print("🚀 PROCESO AUTOMATIZADO DE ACTUALIZACIÓN")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Obtener API key desde variable de entorno (secret de GitHub)
    api_key = os.getenv("GEMINI_API_KEY")
    
    # 1. Scraping
    print("\n📥 PASO 1: Scraping de ADIF...")
    textos_raw = obtener_datos_adif()
    
    if not textos_raw:
        print("⚠️ No se encontraron incidencias. Abortando.")
        return False
    
    print(f"✅ Se descargaron {len(textos_raw)} avisos de la web.")
    
    # 2. Guardar y deduplicar
    print("\n💾 PASO 2: Guardando y deduplicando...")
    num_nuevas, historico = guardar_incidencias(textos_raw)
    print(f"✅ Incidencias nuevas: {num_nuevas}")
    print(f"✅ Total en base de datos: {len(historico)}")
    
    # 3. Análisis con IA
    print("\n🤖 PASO 3: Análisis con IA...")
    analizar_con_ia(historico, api_key)
    
    # Recargar histórico por si hubo cambios
    with open(ARCHIVO_DB, 'r', encoding='utf-8') as f:
        historico = json.load(f)
    
    # 4. Generar JSON para web
    print("\n🌐 PASO 4: Generando incidencias.json para la web...")
    generar_incidencias_web(historico)
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
