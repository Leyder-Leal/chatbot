const dishesList = document.getElementById('dishes');

function attachSubmitListener() {
  const addDishesForm = document.getElementById('add-dish');
  if (addDishesForm) {
    addDishesForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const dishText = document.getElementById('dish').value;

      try {
        const response = await fetch('/dishes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: dishText }),
        });

        if (!response.ok) {
          throw new Error('Error al agregar el plato');
        }

        const data = await response.json();

        if (data.error) {
          console.error('Error:', data.error);
          return;
        }

        const dishElement = document.createElement('li');
        dishElement.textContent = dishText;
        dishesList.appendChild(dishElement);

        addDishesForm.reset();

      } catch (error) {
        console.error('Error al agregar el plato:', error);
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', attachSubmitListener);
