function mostrarContenido() {
    var contenido = document.getElementById("contenido_oculto");
    if (contenido.style.display === "none") {
        contenido.style.display = "block";
    } else {
        contenido.style.display = "none";
    }
}

function mostrarContenido2() {
    var contenido = document.getElementById("contenido_oculto2");
    if (contenido.style.display === "none") {
        contenido.style.display = "block";
    } else {
        contenido.style.display = "none";
    }
}

document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    var formData = new FormData(this);

    // Send form data via AJAX
    fetch('/cuser', {
        method: 'POST',
        body: formData
    })

    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar usuario');
        }
        return response.json();
    })

    .then(data => {
        alert(data.message); // Display success message
        // You can redirect the user or do something else here
    })
    
    .catch(error => {
        alert('Error al registrar usuario: ' + error.message); // Display error message
    });
});

