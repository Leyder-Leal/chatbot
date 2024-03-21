function deleteDish(dishId) {
  fetch(`/dishes/${dishId}`, {
      method: 'DELETE'
  })
  .then(response => {
      if (response.status === 404) {
          throw new Error('El plato no existe');
      }
      if (!response.ok) {
          throw new Error('Error al eliminar el plato');
      }
      // Recarga la página después de eliminar el plato
      window.location.reload();
  })
  .catch(error => {
      console.error('Error al eliminar el plato:', error);
      // Maneja el error apropiadamente
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const addDishForm = document.getElementById('add-dish-form');
  if (addDishForm) {
      addDishForm.addEventListener('submit', async (e) => {
          e.preventDefault();

          const dishName = document.getElementById('dish-name').value;
          const dishPrice = parseFloat(document.getElementById('dish-price').value);
          const dishImageUrl = document.getElementById('dish-image-url').value;

          try {
              const response = await fetch('/dishes', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ name: dishName, price: dishPrice, image_url: dishImageUrl }),
              });

              if (!response.ok) {
                  throw new Error('Error al agregar el plato');
              }

              const data = await response.json();

              if (data.error) {
                  console.error('Error:', data.error);
                  return;
              }

              // Recarga la página después de agregar el plato
              window.location.reload();

          } catch (error) {
              console.error('Error al agregar el plato:', error);
          }
      });
  }
});
