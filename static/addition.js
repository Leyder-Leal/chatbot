const extrasList = document.getElementById('extras');

function attachSubmitListener() {
  const addExtraForm = document.getElementById('add-extra');
  if (addExtraForm) {
    addExtraForm.addEventListener('submit', e => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const extraText = formData.get('extra');

      fetch('/extras', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: extraText }),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('La respuesta de la red no fue correcta');
          }
          return response.json();
        })
        .then(data => {
          const extraElement = document.createElement('li');
          extraElement.textContent = data.text;
          extrasList.appendChild(extraElement);
        })
        .catch(error => {
          console.error('Error al agregar extra:', error);
          // Manejar los errores de forma adecuada (p. ej., mostrar un mensaje al usuario)
        });
    });
  }
}

// Llamar a la función después de DOMContentLoaded
document.addEventListener('DOMContentLoaded', attachSubmitListener);