"""
Script para generar incidencias.json dentro de la carpeta web/
Puede ejecutarse desde GitHub Actions o localmente
"""
import json
import os
import sys
from datetime import datetime

# Ruta relativa desde web/
ARCHIVO_DB = "historico_incidencias.json"
ARCHIVO_WEB = "incidencias.json"

def generar_incidencias_activas():
    """Genera un JSON con solo las incidencias activas para la web"""
    
    # Buscar historico_incidencias.json en varias ubicaciones posibles
    posibles_rutas = [
        ARCHIVO_DB,  # En la misma carpeta web/
        f"../{ARCHIVO_DB}",  # En la carpeta padre
        os.path.join(os.path.dirname(__file__), "..", ARCHIVO_DB)  # Relativo al script
    ]
    
    archivo_encontrado = None
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            archivo_encontrado = ruta
            break
    
    if not archivo_encontrado:
        print(f"[ERROR] No se encontró {ARCHIVO_DB} en ninguna ubicación esperada")
        print(f"Buscado en: {posibles_rutas}")
        return None
    
    print(f"[INFO] Usando archivo: {archivo_encontrado}")
    
    # Cargar histórico completo
    with open(archivo_encontrado, 'r', encoding='utf-8') as f:
        historico = json.load(f)
    
    # Filtrar solo activas que tengan análisis de IA
    incidencias_activas = []
    
    for id_inc, data in historico.items():
        # Verificar que tenga análisis de IA y que esté activa
        if "analisis_ia" in data:
            analisis = data["analisis_ia"]
            # Considerar activa si is_active es True o si status es RED/YELLOW
            if analisis.get("is_active", False) or analisis.get("status") in ["RED", "YELLOW"]:
                incidencia = {
                    "id": id_inc,
                    "summary": analisis.get("summary", ""),
                    "description": analisis.get("description", data.get("descripcion", "")),
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
    
    # Crear objeto final con metadata
    resultado = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(incidencias_activas),
        "incidencias": incidencias_activas
    }
    
    # Guardar en la misma carpeta
    with open(ARCHIVO_WEB, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Generado {ARCHIVO_WEB}")
    print(f"   - Total incidencias activas: {len(incidencias_activas)}")
    
    return resultado

if __name__ == "__main__":
    generar_incidencias_activas()
