// Esperar a que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener('DOMContentLoaded', () => {
  // Obtener el formulario por su id
  const reservationForm = document.getElementById('formulario');

  // Verificar si el formulario existe antes de agregar el evento submit
  if (reservationForm) {
      reservationForm.addEventListener('submit', async (e) => {
          e.preventDefault();

          const nameInput = document.getElementById('name');
          const numberInput = document.getElementById('number');
          const peopleInput = document.getElementById('people');
          const dateInput = document.getElementById('date');

          const reservationData = {
              name: nameInput.value,
              number: numberInput.value,
              people: peopleInput.value,
              date: dateInput.value
          };

          addReservation(reservationData, reservationForm);
      });
  }
});

function addReservation(reservationData, reservationForm) {
  fetch('/reservations', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(reservationData),
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Error al agregar la reservación');
      }
      return response.json();
  })
  .then(data => {
      if (data.success) {
          // Mostrar mensaje de confirmación
          document.getElementById('mensaje-confirmacion').style.display = 'block';
          // Limpiar el formulario después de 2 segundos
          setTimeout(() => {
              document.getElementById('mensaje-confirmacion').style.display = 'none';
              reservationForm.reset();
          }, 2000);
      } else {
          console.error('Error:', data.error);
      }
  })
  .catch(error => {
      console.error('Error al agregar la reservación', error);
  });
}
