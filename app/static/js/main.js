document.getElementById('resume-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });
    const resultDiv = document.getElementById('result');
    if (response.ok) {
        const data = await response.json();
        resultDiv.textContent = JSON.stringify(data, null, 2);
    } else {
        const err = await response.json();
        resultDiv.textContent = 'Error: ' + (err.error || 'unknown');
    }
});
