
export function formatTimeRate(rate) { //Place here
    if (rate < 60) {
        return `${rate}x faster`;
    } else if (rate < 3600) {
        const minutes = Math.floor(rate / 60);
        return `${rate}x faster (1 second = ${minutes} minute${minutes > 1 ? 's' : ''})`;
    } else if (rate < 86400) {
        const hours = Math.floor(rate / 3600);
        return `${rate}x faster (1 second = ${hours} hour${hours > 1 ? 's' : ''})`;
    } else {
        const days = Math.floor(rate / 86400);
        return `${rate}x faster (1 second = ${days} day${days > 1 ? 's' : ''})`;
    }
}



export function updateGameTime() {
    const gameTimeSpan = document.getElementById('game-time');
    const timeRateSpan = document.getElementById('time-rate');

    


    fetch('/gametime/get_time_info') // New Flask route to get time info
        .then(response => response.json())
        .then(data => {
            if (data.game_time && data.time_rate) {
                gameTimeSpan.textContent = "Game Time: " + data.game_time;
                timeRateSpan.textContent = "Rate: " + formatTimeRate(data.time_rate);
            } else {
                console.error("Invalid data received from server:", data);
                gameTimeSpan.textContent = "Game Time: Error"; // Indicate an error
                timeRateSpan.textContent = "Rate: Error";       // Indicate an error
            }
        })
        .catch(error => {
            console.error('Error fetching game time:', error);
            gameTimeSpan.textContent = "Game Time: Error"; // Display error message
            timeRateSpan.textContent = "Rate: Error";       // Display error message
        });
}

updateGameTime();
setInterval(updateGameTime, 3000);