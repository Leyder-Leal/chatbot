function attachSubmitListener() {
  const addDishesForm = document.getElementById('add-dish');
  if (addDishesForm) {
    addDishesForm.addEventListener('submit', async (e) => {
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
}

document.addEventListener('DOMContentLoaded', attachSubmitListener);
