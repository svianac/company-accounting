document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('entryForm');
    const entriesList = document.getElementById('entriesList');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const date = document.getElementById('date').value;
        const amount = document.getElementById('amount').value;
        const comments = document.getElementById('comments').value;

        if (date && amount) {
            const entryItem = document.createElement('li');
            entryItem.textContent = `${date} - $${amount} - ${comments}`;
            entriesList.appendChild(entryItem);

            form.reset();
        } else {
            alert('Please fill in all required fields.');
        }
    });
});