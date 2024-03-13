const optionsList = document.getElementById('options');
const addOptionForm = document.getElementById('add-option');

// Obtiene la lista de opciones al cargar la página
fetch('/options')
    .then(response => response.json())
    .then(data => {
        data.forEach(option => {
            const optionElement = document.createElement('li');
            optionElement.textContent = option.text;
            optionsList.appendChild(optionElement);
        });
    });

// Agrega una nueva opción
addOptionForm.addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const optionText = formData.get('option');

    fetch('/options', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: optionText }),
    })
        .then(response => response.json())
        .then(data => {
            const optionElement = document.createElement('li');
            optionElement.textContent = data.text;
            optionsList.appendChild(optionElement);
        });
});