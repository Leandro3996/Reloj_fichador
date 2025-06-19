/**
 * SISTEMA DE CONTROL DE ASISTENCIA - RRHH
 * JavaScript principal para la interfaz moderna
 */

// Configuración global
const RRHHApp = {
    config: {
        updateInterval: 300000, // 5 minutos
        dateFormat: 'DD/MM/YYYY',
        timeFormat: 'HH:mm',
        locale: 'es-AR'
    },

    // Cache para datos
    cache: {
        operarios: null,
        areas: null,
        lastUpdate: null
    }
};

/**
 * Inicialización de la aplicación
 */
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 Inicializando RRHH Sistema...');

    // Configurar librerías externas
    setupDataTables();
    setupBootstrapComponents();
    setupAjaxDefaults();

    // Configurar eventos globales
    setupGlobalEvents();

    // Inicializar componentes específicos
    initializeSpecificComponents();

    console.log('✅ RRHH Sistema inicializado correctamente');
}

/**
 * Configuración de DataTables
 */
function setupDataTables() {
    // Configuración global de DataTables en español
    $.extend(true, $.fn.dataTable.defaults, {
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        },
        responsive: true,
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
            '<"row"<"col-sm-12"tr>>' +
            '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
        buttons: [
            {
                extend: 'excel',
                text: '<i class="bi bi-file-earmark-excel me-1"></i>Excel',
                className: 'btn btn-success btn-sm',
                exportOptions: {
                    columns: ':not(.no-export)'
                }
            },
            {
                extend: 'pdf',
                text: '<i class="bi bi-file-earmark-pdf me-1"></i>PDF',
                className: 'btn btn-danger btn-sm',
                exportOptions: {
                    columns: ':not(.no-export)'
                }
            },
            {
                extend: 'print',
                text: '<i class="bi bi-printer me-1"></i>Imprimir',
                className: 'btn btn-secondary btn-sm'
            }
        ]
    });
}

/**
 * Configuración de componentes de Bootstrap
 */
function setupBootstrapComponents() {
    // Inicializar tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Configuración AJAX por defecto
 */
function setupAjaxDefaults() {
    // CSRF Token para Django
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Manejador global de errores AJAX
    $(document).ajaxError(function (event, xhr, settings, error) {
        console.error('Error AJAX:', error);
        showAlert('Error de conexión. Intente nuevamente.', 'danger');
    });
}

/**
 * Configuración de eventos globales
 */
function setupGlobalEvents() {
    // Actualización automática cada 5 minutos
    setInterval(function () {
        updateDashboardData();
    }, RRHHApp.config.updateInterval);

    // Evento para mostrar loading en formularios
    $('form').on('submit', function () {
        const submitBtn = $(this).find('button[type="submit"]');
        const originalText = submitBtn.html();

        submitBtn.html('<span class="loading-spinner me-2"></span>Procesando...');
        submitBtn.prop('disabled', true);

        // Restaurar después de 10 segundos (fallback)
        setTimeout(() => {
            submitBtn.html(originalText);
            submitBtn.prop('disabled', false);
        }, 10000);
    });

    // Auto-hide alerts después de 5 segundos
    $('.alert:not(.alert-permanent)').delay(5000).fadeOut('slow');
}

/**
 * Inicializar componentes específicos según la página
 */
function initializeSpecificComponents() {
    const currentPage = getCurrentPage();

    switch (currentPage) {
        case 'dashboard':
            initializeDashboard();
            break;
        case 'operarios':
            initializeOperarios();
            break;
        case 'asistencia':
            initializeAsistencia();
            break;
        case 'reportes':
            initializeReportes();
            break;
        default:
            console.log('Página no requiere inicialización específica');
    }
}

/**
 * Obtener página actual basada en la URL
 */
function getCurrentPage() {
    const path = window.location.pathname;

    if (path.includes('/rrhh/operarios/')) return 'operarios';
    if (path.includes('/rrhh/asistencia/')) return 'asistencia';
    if (path.includes('/rrhh/reportes/')) return 'reportes';
    if (path.includes('/rrhh/')) return 'dashboard';

    return 'unknown';
}

/**
 * Inicialización específica del Dashboard
 */
function initializeDashboard() {
    console.log('📊 Inicializando Dashboard...');

    // Configurar actualización de gráficos
    setupChartUpdates();

    // Configurar filtros del dashboard
    setupDashboardFilters();
}

/**
 * Inicialización específica de Operarios
 */
function initializeOperarios() {
    console.log('👥 Inicializando módulo de Operarios...');

    // La tabla de operarios se inicializa específicamente en su template
    // para permitir configuraciones personalizadas
}

/**
 * Inicialización específica de Asistencia
 */
function initializeAsistencia() {
    console.log('📅 Inicializando módulo de Asistencia...');

    // Configurar tabla de asistencia solo si no tiene una clase especial para manejo customizado
    if ($('#asistenciaTable').length && !$('#asistenciaTable').hasClass('custom-datatable')) {
        $('#asistenciaTable').DataTable({
            processing: true,
            serverSide: false,
            responsive: true,
            order: [[3, 'desc']], // Ordenar por fecha
            buttons: ['excel', 'pdf', 'print']
        });
    }

    // Configurar filtros de fecha
    setupDateFilters();
}

/**
 * Inicialización específica de Reportes
 */
function initializeReportes() {
    console.log('📈 Inicializando módulo de Reportes...');

    // Configurar generación de reportes
    setupReportGeneration();
}

/**
 * Configuración de filtros de fecha
 */
function setupDateFilters() {
    // Configurar date pickers si existen
    $('input[type="date"]').each(function () {
        // Establecer fecha máxima como hoy
        $(this).attr('max', new Date().toISOString().split('T')[0]);
    });
}

/**
 * Configuración de actualización de gráficos
 */
function setupChartUpdates() {
    // Configurar botones de período para gráficos
    $('input[name="periodoAsistencia"]').on('change', function () {
        const periodo = $(this).attr('id');
        updateChartPeriod(periodo);
    });
}

/**
 * Configuración de filtros del dashboard
 */
function setupDashboardFilters() {
    $('#filtrosDashboard').on('submit', function (e) {
        e.preventDefault();
        aplicarFiltrosDashboard();
    });
}

/**
 * Actualizar período del gráfico
 */
function updateChartPeriod(periodo) {
    console.log('Actualizando gráfico para período:', periodo);

    // Aquí iría la lógica para actualizar el gráfico via AJAX
    $.ajax({
        url: '/rrhh/api/dashboard-data/',
        data: { periodo: periodo },
        success: function (response) {
            // Actualizar gráfico con nuevos datos
            updateChart(response.data);
        },
        error: function () {
            showAlert('Error al actualizar el gráfico', 'warning');
        }
    });
}

/**
 * Actualizar datos del dashboard
 */
function updateDashboardData() {
    if (getCurrentPage() !== 'dashboard') return;

    console.log('🔄 Actualizando datos del dashboard...');

    $.ajax({
        url: '/rrhh/api/dashboard-data/',
        success: function (response) {
            // Actualizar KPIs
            updateKPIs(response.kpis);

            // Actualizar tablas
            updateDashboardTables(response.tables);

            // Mostrar última actualización
            $('#lastUpdate').text('Actualizado: ' + new Date().toLocaleTimeString());
        },
        error: function () {
            console.warn('Error al actualizar dashboard automáticamente');
        }
    });
}

/**
 * Aplicar filtros del dashboard
 */
function aplicarFiltrosDashboard() {
    const formData = new FormData(document.getElementById('filtrosDashboard'));
    const params = new URLSearchParams(formData);

    // Mostrar loading
    showLoading();

    // Redirigir con filtros
    window.location.href = '/rrhh/?' + params.toString();
}

/**
 * Mostrar alertas
 */
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    // Agregar al contenedor de alertas o al inicio del contenido
    const container = $('.main-content .container-fluid').first();
    container.prepend(alertHtml);

    // Auto-hide después de 5 segundos
    setTimeout(() => {
        $('.alert').last().fadeOut();
    }, 5000);
}

/**
 * Obtener icono para alertas
 */
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'danger': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Mostrar loading global
 */
function showLoading() {
    const loadingHtml = `
        <div id="globalLoading" class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" style="background: rgba(255,255,255,0.8); z-index: 9999;">
            <div class="text-center">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <div>Procesando...</div>
            </div>
        </div>
    `;

    $('body').append(loadingHtml);
}

/**
 * Ocultar loading global
 */
function hideLoading() {
    $('#globalLoading').remove();
}

/**
 * Utilidades
 */

// Obtener cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Verificar si método es CSRF safe
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Formatear números
function formatNumber(num) {
    return new Intl.NumberFormat('es-AR').format(num);
}

// Formatear fechas
function formatDate(date, format = 'DD/MM/YYYY') {
    return new Date(date).toLocaleDateString('es-AR');
}

// Formatear horas
function formatTime(time) {
    return new Date(time).toLocaleTimeString('es-AR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Exportar funciones globales
 */
window.RRHHApp = RRHHApp;
window.showAlert = showAlert;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.formatNumber = formatNumber;
window.formatDate = formatDate;
window.formatTime = formatTime;
