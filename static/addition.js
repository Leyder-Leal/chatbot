const additionsList = document.getElementById('additions');

function attachSubmitListener() {
  const addAdditionForm = document.getElementById('add-addition');
  if (addAdditionForm) {
    addAdditionForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const additionText = document.getElementById('addition').value;

      try {
        const response = await fetch('/additions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: additionText }),
        });

        if (!response.ok) {
          throw new Error('Error al agregar adición');
        }

        const data = await response.json();

        if (data.error) {
          console.error('Error:', data.error);
          return;
        }

        const additionElement = document.createElement('li');
        additionElement.textContent = additionText;
        additionsList.appendChild(additionElement);

        addAdditionForm.reset();

      } catch (error) {
        console.error('Error al agregar adición:', error);
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', attachSubmitListener);
