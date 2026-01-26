// Datos globales
let incidenciasData = [];
let incidenciasFiltradas = [];

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
        
        // Actualizar fecha
        document.getElementById('last-update').textContent = data.generated_at || '-';
        
        // Actualizar estadísticas
        actualizarEstadisticas();
        
        // Renderizar tabla
        renderizarTabla();
        
        // Configurar filtros
        configurarFiltros();
        
    } catch (error) {
        console.error('Error cargando datos:', error);
        document.getElementById('table-body').innerHTML = 
            '<tr><td colspan="7" class="no-results">Error cargando datos</td></tr>';
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
        tbody.innerHTML = '<tr><td colspan="7" class="no-results">No hay incidencias que coincidan con los filtros</td></tr>';
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
        
        return `
            <tr>
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td><span class="network-badge">${networkText}</span></td>
                <td>${line}</td>
                <td>${nodes}</td>
                <td>${inc.summary || inc.description.substring(0, 100)}</td>
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

// Inicializar cuando carga la página
document.addEventListener('DOMContentLoaded', cargarDatos);
