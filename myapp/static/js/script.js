const sendDataButton = document.getElementById('sendDataButton');
const input_data = document.getElementById('input_area');
const resultDiv = document.getElementById('result');

sendDataButton.addEventListener('click', async () => {
    const message = 'Hello from JavaScript!';
    try {
        const response = await fetch('/api/data2', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "message": message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        resultDiv.textContent = data.result;

    } catch (error) {
        resultDiv.textContent = `Error: ${error}`;
    }
});