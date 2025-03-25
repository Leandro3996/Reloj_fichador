/* 
 * JavaScript para el calendario de días feriados
 */
document.addEventListener('DOMContentLoaded', function () {
    // Pre-rellenar la fecha cuando se crea un nuevo feriado desde el calendario
    const urlParams = new URLSearchParams(window.location.search);
    const fechaParam = urlParams.get('fecha');

    if (fechaParam && document.getElementById('id_fecha')) {
        document.getElementById('id_fecha').value = fechaParam;
    }

    // Si estamos en la página de cambios, añadir estilos adicionales
    if (document.querySelector('.feriados-calendar')) {
        // Añadir clases CSS a las celdas del calendario según su estado
        const celdas = document.querySelectorAll('.feriados-calendar td');
        celdas.forEach(function (celda) {
            // Aquí podrías añadir lógica para styling dinámico adicional
        });
    }
}); 