function attachSubmitListener() {
  const addOrdersForm = document.getElementById('add-order');
  if (addOrdersForm) {
      addOrdersForm.addEventListener('submit', async (e) => {
          e.preventDefault();

          const formData = new FormData(addOrdersForm);
          const ticketText = formData.get('ticket');
          const clientText = formData.get('client');
          const addressText = formData.get('address');
          const dishText = formData.get('dish');
          const additionText = formData.get('addition');

          try {
              const response = await fetch('/orders', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ticket: ticketText, client: clientText, address: addressText, dish: dishText, addition: additionText}),
              });

              if (!response.ok) {
                  throw new Error('Error al agregar el pedido');
              }

              const data = await response.json();

              if (data.error) {
                  console.error('Error:', data.error);
                  return;
              }

              // Puedes hacer algo con la respuesta si lo necesitas
              console.log('Pedido agregado correctamente:', data);

              // Limpiar el formulario
              addOrdersForm.reset();

          } catch (error) {
              console.error('Error al agregar el pedido:', error);
          }
      });
  }
}

document.addEventListener('DOMContentLoaded', attachSubmitListener);
