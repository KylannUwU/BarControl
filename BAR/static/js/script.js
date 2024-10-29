function updateProgress(value) {
    console.log(`Actualizando progreso a: ${value}`); // Añadido para depuración
    fetch(`/update_progress/${value}`)
        .then(response => response.json())
        .then(data => {
            const percentage = data.percentage;
            const currentValue = data.current_value;

            // Actualizar la barra de progreso
            document.querySelector('.progress-bar-fill').style.width = percentage + '%';
            document.getElementById('progress-number').innerText = Math.floor(currentValue);

            // Mover la imagen a la posición correcta
            const arrow = document.querySelector('.progress-arrow');
            arrow.style.left = `calc(${percentage}% - 30px)`; // Ajusta la posición de la flecha
        })
        .catch(error => console.error('Error:', error));
}

// Asegúrate de que la barra de progreso se inicialice en 5000
