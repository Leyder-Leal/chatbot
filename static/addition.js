// Esta función elimina una adición
async function deleteAddition(additionId) {
  try {
      const response = await fetch(`/additions/${additionId}`, {
          method: 'DELETE'
      });

      if (!response.ok) {
          throw new Error('Error al eliminar la adición');
      }
      window.location.reload();
  } catch (error) {
      console.error('Error al eliminar la adición:', error);
  }
}

function attachSubmitListener() {
  const addAdditionsForm = document.getElementById('add-addition');
  if (addAdditionsForm) {
      addAdditionsForm.addEventListener('submit', async (e) => {
          e.preventDefault();

          const additionName = document.getElementById('addition-name').value;
          const additionPrice = parseFloat(document.getElementById('addition-price').value);
          const additionImageUrl = document.getElementById('addition-image-url').value;

          try {
              const response = await fetch('/additions', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ name: additionName, price: additionPrice, image_url: additionImageUrl }),
              });

              if (!response.ok) {
                  throw new Error('Error al agregar la adición');
              }

              const data = await response.json();

              if (data.error) {
                  console.error('Error:', data.error);
                  return;
              }

              // Recarga la página después de agregar la adición
              window.location.reload();

          } catch (error) {
              console.error('Error al agregar la adición:', error);
          }
      });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  attachSubmitListener();
});
