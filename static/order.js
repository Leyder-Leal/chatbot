// order.js

function updateOrderStatusInUI(orderId, newStatus) {
    const orderStatusElement = document.getElementById(`order-status-${orderId}`);
    if (orderStatusElement) {
        orderStatusElement.textContent = newStatus;
    }
}

async function deleteOrder(orderId) {
    try {
        const response = await fetch(`/orders/${orderId}`, {
            method: 'DELETE'
        });

        if (response.status === 404) {
            console.warn('El pedido ya ha sido eliminado o no existe.');
            // No es un error, simplemente el recurso no se encontró
            return;
        }

        if (!response.ok) {
            throw new Error('Error al eliminar el pedido');
        }

        // Si llegamos aquí, la eliminación fue exitosa
        window.location.reload();
    } catch (error) {
        console.error('Error al eliminar el pedido:', error);
    }
}

async function updateOrderStatus(orderId, orderStatus) {
    try {
        const response = await fetch(`/orders/${orderId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: orderStatus }),
        });

        if (!response.ok) {
            throw new Error('Error al actualizar el estado del pedido');
        }

        const data = await response.json();

        if (data.error) {
            console.error('Error:', data.error);
            return;
        }

        console.log('Estado del pedido actualizado correctamente:', data);

        updateOrderStatusInUI(orderId, orderStatus);

        await refreshOrders();

    } catch (error) {
        console.error('Error al actualizar el estado del pedido:', error);
    }
}

function createOrderListItem(order) {
    const listItem = document.createElement('li');
    listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
    listItem.innerHTML = `Ticket: ${order.ticket}, Cliente: ${order.client}, Dirección: ${order.address}, Plato: ${order.dish}, Adición: ${order.addition}, estado: ${order.status}`;

    const updateForm = document.createElement('form');
    updateForm.id = `update-order-${order.id}`;
    updateForm.innerHTML = `
        <select name="status" class="form-control">
            <option value="preparando">Preparando</option>
            <option value="en camino">En Camino</option>
            <option value="entregado">Entregado</option>
        </select>
        <button type="submit" class="btn btn-primary">Actualizar Estado</button>
    `;

    updateForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(updateForm);
        const orderStatus = formData.get('status');

        await updateOrderStatus(order.id, orderStatus);
    });

    const deleteButton = document.createElement('button');
    deleteButton.className = 'btn btn-danger';
    deleteButton.textContent = 'Eliminar';
    deleteButton.addEventListener('click', () => deleteOrder(order.id));

    listItem.appendChild(updateForm);
    listItem.appendChild(deleteButton);

    return listItem;
}

async function refreshOrders() {
    try {
        const response = await fetch('/orders');
        const ordersData = await response.json();

        if (!response.ok) {
            throw new Error('Error al cargar los pedidos');
        }

        const ordersList = document.getElementById('orders');
        ordersList.innerHTML = '';

        ordersData.forEach(order => {
            const listItem = createOrderListItem(order);
            ordersList.appendChild(listItem);
        });

    } catch (error) {
        console.error('Error al cargar los pedidos:', error);
    }
}

async function addOrder() {
    const orderTicket = document.getElementById('order-ticket').value;
    const orderClient = document.getElementById('order-client').value;
    const orderAddress = document.getElementById('order-address').value;
    const orderDish = document.getElementById('order-dish').value;
    const orderAddition = document.getElementById('order-addition').value;
    const orderStatus = document.getElementById('order-status').value;

    try {
        const response = await fetch('/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticket: orderTicket, client: orderClient, address: orderAddress, dish: orderDish, addition: orderAddition, status: orderStatus }),
        });

        if (!response.ok) {
            throw new Error('Error al agregar el pedido');
        }

        const data = await response.json();

        if (data.error) {
            console.error('Error:', data.error);
            return;
        }

        window.location.reload();

    } catch (error) {
        console.error('Error al agregar el pedido:', error);
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await refreshOrders();

    const addOrderForm = document.getElementById('add-order');
    if (addOrderForm) {
        addOrderForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await addOrder();
        });
    }
});
