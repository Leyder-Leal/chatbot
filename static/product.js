function attachSubmitListener() {
    const addProductForm = document.getElementById('add-product');
    if (addProductForm) {
        addProductForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const productName = document.getElementById('product-name').value;
            const productDescription = document.getElementById('product-description').value;
            const productPrice = parseFloat(document.getElementById('product-price').value);
            const productImageUrl = document.getElementById('product-image-url').value;
            const productDetailsUrl = document.getElementById('product-details-url').value;
            const productDetailsPayload = document.getElementById('product-details-payload').value;

            try {
                const response = await fetch('/products', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        name: productName, 
                        description: productDescription,
                        price: productPrice, 
                        image_url: productImageUrl,
                        details_url: productDetailsUrl,
                        details_payload: productDetailsPayload
                    }),
                });

                if (!response.ok) {
                    throw new Error('Error al agregar el producto');
                }

                const data = await response.json();

                if (data.error) {
                    console.error('Error:', data.error);
                    return;
                }

                // Recarga la página después de agregar el producto
                window.location.reload();

            } catch (error) {
                console.error('Error al agregar el producto:', error);
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', attachSubmitListener);

async function deleteProduct(productId) {
    try {
        const response = await fetch(`/products/${productId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Error al eliminar el producto');
        }

        // Recarga la página después de eliminar el producto
        window.location.reload();
    } catch (error) {
        console.error('Error al eliminar el producto:', error);
    }
}
