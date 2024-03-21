document.addEventListener('DOMContentLoaded', () => {
  fetch('/reservationlist')
  .then(response => response.json())
  .then(reservations => {
      const reservationsContainer = document.getElementById('reservations-container');

      reservations.forEach(reservation => {
          const reservationCard = createReservationCard(reservation);
          reservationsContainer.appendChild(reservationCard);
      });
  })
  .catch(error => console.error('Error al cargar las reservaciones:', error));
});

function createReservationCard(reservation) {
  const card = document.createElement('div');
  card.classList.add('card', 'reservation-card');

  const cardBody = document.createElement('div');
  cardBody.classList.add('card-body');

  const name = document.createElement('h5');
  name.classList.add('card-title');
  name.textContent = reservation.name;

  const number = document.createElement('p');
  number.classList.add('card-text');
  number.textContent = 'Número telefónico: ' + reservation.number;

  const people = document.createElement('p');
  people.classList.add('card-text');
  people.textContent = 'Cantidad de personas: ' + reservation.people;

  const date = document.createElement('p');
  date.classList.add('card-text');
  date.textContent = 'Fecha: ' + reservation.date;

  const deleteButton = document.createElement('button');
  deleteButton.classList.add('btn', 'btn-danger');
  deleteButton.textContent = 'Eliminar';
  deleteButton.addEventListener('click', () => deleteReservation(reservation.id));

  cardBody.appendChild(name);
  cardBody.appendChild(number);
  cardBody.appendChild(people);
  cardBody.appendChild(date);
  cardBody.appendChild(deleteButton);

  card.appendChild(cardBody);

  return card;
}

function deleteReservation(reservationId) {
  fetch(`/reservations/${reservationId}`, {
      method: 'DELETE'
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // Eliminar la tarjeta de reservación del DOM
          const cardToRemove = document.querySelector(`.reservation-card[data-id="${reservationId}"]`);
          cardToRemove.remove();
      } else {
          alert('Error al eliminar la reservación. Por favor, intenta de nuevo.');
      }
  })
  .catch(error => console.error('Error al eliminar la reservación:', error));
}
