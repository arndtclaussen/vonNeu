export function updateGameLog() {
    fetch('/gamelog/get_logs')
        .then(response => response.json())
        .then(logs => {
            const gameLogList = document.getElementById('game-log-list');
            gameLogList.innerHTML = ''; // Clear existing logs

            logs.forEach(log => {
                const li = document.createElement('li');

                li.textContent = `${log.timestamp} - ${log.message}`;

                gameLogList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching game logs:', error);
        });
}

/*
updateGameLog();
setInterval(updateGameLog, 3000); 
*/