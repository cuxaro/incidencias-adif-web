// Datos globales
let incidenciasData = [];
let incidenciasFiltradas = [];
let ultimaFechaConocida = null; // Para detectar cambios
let intervaloActualizacion = null; // Referencia al intervalo

// Mapeo de redes
const networkNames = {
    'CERCANIAS_MADRID': 'Cercanías Madrid',
    'CERCANIAS_VALENCIA': 'Cercanías Valencia',
    'RODALIES_CATALUNYA': 'Rodalies Catalunya',
    'ALTA_VELOCIDAD': 'Alta Velocidad',
    'MEDIA_DISTANCIA': 'Media Distancia',
    'ANCHO_METRICO': 'Ancho Métrico',
    'OTROS': 'Otros'
};

// Mapeo de estados
const statusNames = {
    'RED': 'Interrupción',
    'YELLOW': 'Retrasos',
    'BLUE': 'Obras/Alternativa',
    'GREEN': 'Subsanada'
};

// Cargar datos
async function cargarDatos() {
    try {
        // Cache busting: añadir timestamp para forzar descarga de versión actualizada
        const response = await fetch(`incidencias.json?v=${Date.now()}`);
        const data = await response.json();
        
        incidenciasData = data.incidencias || [];
        incidenciasFiltradas = [...incidenciasData];
        
        // Actualizar fecha - convertir a hora de España (CET/CEST)
        const fechaEspana = convertirAHoraEspana(data.generated_at);
        document.getElementById('last-update').textContent = fechaEspana || '-';
        
        // Guardar fecha para comparación futura
        ultimaFechaConocida = data.generated_at;
        
        // Actualizar estadísticas
        actualizarEstadisticas();
        
        // Renderizar tabla
        renderizarTabla();
        
        // Configurar filtros
        configurarFiltros();
        
    } catch (error) {
        console.error('Error cargando datos:', error);
        document.getElementById('table-body').innerHTML = 
            '<tr><td colspan="8" class="no-results">Error cargando datos</td></tr>';
    }
}

// Actualizar estadísticas
function actualizarEstadisticas() {
    const total = incidenciasFiltradas.length;
    const red = incidenciasFiltradas.filter(i => i.status === 'RED').length;
    const yellow = incidenciasFiltradas.filter(i => i.status === 'YELLOW').length;
    
    document.getElementById('total-incidencias').textContent = total;
    document.getElementById('total-red').textContent = red;
    document.getElementById('total-yellow').textContent = yellow;
}

// Renderizar tabla
function renderizarTabla() {
    const tbody = document.getElementById('table-body');
    
    if (incidenciasFiltradas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="no-results">No hay incidencias que coincidan con los filtros</td></tr>';
        return;
    }
    
    tbody.innerHTML = incidenciasFiltradas.map(inc => {
        const statusClass = `status-${inc.status.toLowerCase()}`;
        const statusText = statusNames[inc.status] || inc.status;
        const networkText = networkNames[inc.network] || inc.network;
        const severity = inc.severity_level || 1;
        const nodes = inc.nodes && inc.nodes.length > 0 ? inc.nodes.join(', ') : '-';
        const line = inc.line_affected || '-';
        const startDate = inc.start_date || '-';
        const descripcionOriginal = inc.descripcion_original || inc.description || '-';
        
        return `
            <tr>
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td><span class="network-badge">${networkText}</span></td>
                <td>${line}</td>
                <td>${nodes}</td>
                <td>${inc.summary || inc.description.substring(0, 100)}</td>
                <td class="descripcion-cell">${descripcionOriginal}</td>
                <td><span class="severity severity-${severity}">
                    <span class="severity-dot"></span>
                    <span class="severity-dot"></span>
                    <span class="severity-dot"></span>
                    <span class="severity-dot"></span>
                    <span class="severity-dot"></span>
                </span></td>
                <td>${startDate}</td>
            </tr>
        `;
    }).join('');
}

// Configurar filtros
function configurarFiltros() {
    const searchInput = document.getElementById('search-input');
    const filterNetwork = document.getElementById('filter-network');
    const filterStatus = document.getElementById('filter-status');
    
    function aplicarFiltros() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const networkFilter = filterNetwork.value;
        const statusFilter = filterStatus.value;
        
        incidenciasFiltradas = incidenciasData.filter(inc => {
            // Filtro de búsqueda
            if (searchTerm) {
                const searchable = [
                    inc.summary || '',
                    inc.description || '',
                    inc.line_affected || '',
                    (inc.nodes || []).join(' ')
                ].join(' ').toLowerCase();
                
                if (!searchable.includes(searchTerm)) {
                    return false;
                }
            }
            
            // Filtro de red
            if (networkFilter && inc.network !== networkFilter) {
                return false;
            }
            
            // Filtro de estado
            if (statusFilter && inc.status !== statusFilter) {
                return false;
            }
            
            return true;
        });
        
        actualizarEstadisticas();
        renderizarTabla();
    }
    
    searchInput.addEventListener('input', aplicarFiltros);
    filterNetwork.addEventListener('change', aplicarFiltros);
    filterStatus.addEventListener('change', aplicarFiltros);
}

// Convertir timestamp a hora de España (CET/CEST)
function convertirAHoraEspana(timestamp) {
    if (!timestamp) return '-';
    
    try {
        // Parsear el timestamp (formato: "YYYY-MM-DD HH:MM:SS")
        // Asumimos que viene en UTC (desde GitHub Actions)
        const [fecha, hora] = timestamp.split(' ');
        const [year, month, day] = fecha.split('-').map(Number);
        const [hours, minutes, seconds] = hora.split(':').map(Number);
        
        // Crear fecha en UTC
        const fechaUTC = new Date(Date.UTC(year, month - 1, day, hours, minutes, seconds || 0));
        
        // Convertir a hora de España usando Intl.DateTimeFormat
        const formatter = new Intl.DateTimeFormat('es-ES', {
            timeZone: 'Europe/Madrid',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        });
        
        // Formatear la fecha
        const partes = formatter.formatToParts(fechaUTC);
        const fechaEspana = {
            year: partes.find(p => p.type === 'year').value,
            month: partes.find(p => p.type === 'month').value,
            day: partes.find(p => p.type === 'day').value,
            hour: partes.find(p => p.type === 'hour').value,
            minute: partes.find(p => p.type === 'minute').value,
            second: partes.find(p => p.type === 'second').value
        };
        
        return `${fechaEspana.year}-${fechaEspana.month}-${fechaEspana.day} ${fechaEspana.hour}:${fechaEspana.minute}:${fechaEspana.second}`;
    } catch (error) {
        console.error('Error convirtiendo hora:', error);
        return timestamp; // Devolver original si hay error
    }
}

// Verificar si hay actualizaciones disponibles
async function verificarActualizaciones() {
    try {
        // Hacer fetch solo para obtener el generated_at sin cache
        const response = await fetch(`incidencias.json?v=${Date.now()}`);
        const data = await response.json();
        
        // Comparar con la fecha conocida
        if (ultimaFechaConocida && data.generated_at !== ultimaFechaConocida) {
            console.log('🔄 Nueva actualización detectada, recargando datos...');
            // Recargar todos los datos
            await cargarDatos();
        }
    } catch (error) {
        console.error('Error verificando actualizaciones:', error);
    }
}

// Iniciar verificación periódica cada 1 minuto
function iniciarVerificacionPeriodica() {
    // Verificar cada 1 minuto (60000 ms)
    intervaloActualizacion = setInterval(verificarActualizaciones, 60 * 1000);
    console.log('✅ Verificación automática iniciada (cada 1 minuto)');
}

// Detener verificación periódica (útil si se necesita)
function detenerVerificacionPeriodica() {
    if (intervaloActualizacion) {
        clearInterval(intervaloActualizacion);
        intervaloActualizacion = null;
        console.log('⏸️ Verificación automática detenida');
    }
}

// Inicializar cuando carga la página
document.addEventListener('DOMContentLoaded', () => {
    cargarDatos().then(() => {
        // Iniciar verificación periódica después de cargar los datos iniciales
        iniciarVerificacionPeriodica();
    });
});
