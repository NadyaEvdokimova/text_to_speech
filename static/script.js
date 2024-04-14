document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        fetch('/', {
            method: 'POST',
            body: new FormData(event.target)
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                console.error('Request failed with status ' + response.status);
                throw new Error('Request failed with status ' + response.status);
            }
        })
        .then(blob => {
            const audioUrl = URL.createObjectURL(blob);
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.src = audioUrl;
            audioPlayer.style.display = 'block';
            return blob.text(); // Get the response text
        })
        .then(responseText => {
            // Check if the response text contains "ERROR"
            if (responseText && responseText.includes("ERROR")) {
                throw new Error('An error occurred while processing your request.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Display error message to the user
            const alertDiv = document.createElement('div');
            alertDiv.classList.add('alert', 'alert-danger');
            alertDiv.textContent = error.message;
            document.querySelector('.container_part').prepend(alertDiv);
        });
    });

});

