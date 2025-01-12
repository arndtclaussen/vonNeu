export function updateGameLog() {
    fetch('/gamelog/get_logs')
        .then(response => response.json())
        .then(logs => {
            const gameLogList = document.getElementById('game-log-list');
            gameLogList.innerHTML = ''; // Clear existing logs

            logs.forEach(log => {
                const li = document.createElement('li');
                // Format the timestamp.  The JSON likely gives it to you as a string already formatted, but if it's a numeric timestamp, you'll need JavaScript's Date object.
                // Example for numeric timestamp:
                // const timestamp = new Date(log.timestamp * 1000); // Assuming timestamp is in seconds, multiply by 1000 for milliseconds
                // li.textContent = `${timestamp.toUTCString()} - ${log.message}`;

                // Example for already formatted string timestamp:
                li.textContent = `${log.timestamp} - ${log.message}`;



                gameLogList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching game logs:', error);
        });
}



updateGameLog();
setInterval(updateGameLog, 5000); // Poll every 5 seconds