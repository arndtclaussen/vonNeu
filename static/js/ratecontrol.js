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


export function updateTimeRate() {
    
    const timeRateSpan = document.getElementById('time-rate');

    fetch('/gametime/get_time_info') // New Flask route to get time info
        .then(response => response.json())
        .then(data => {
            if (data.time_rate) {
                
                timeRateSpan.textContent = "Rate: " + formatTimeRate(data.time_rate);
            } else {
                console.error("Invalid data received from server:", data);
                timeRateSpan.textContent = "Rate: Error";       // Indicate an error
            }
        })
        .catch(error => {
            console.error('Error fetching game time:', error);
            timeRateSpan.textContent = "Rate: Error";       // Display error message
        });
}





document.addEventListener('DOMContentLoaded', () => {

    const rateResetButton = document.getElementById('rate-reset'); 


    const ratePlusButton = document.getElementById('rate-plus');
    const ratePlusButton10 = document.getElementById('rate-plus+10');
    const ratePlusButton100 = document.getElementById('rate-plus+100');
    const ratePlusButton1000 = document.getElementById('rate-plus+1000');


    function updateRate(change) {
        fetch('/gametime/update_rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ change: change })
        })
            .then(response => {  // No need to parse JSON
                if (response.ok) {
                    console.log("Rate change request successful");
                    updateTimeRate(); // Immediately refresh the display after successful change
                } else {
                    console.error("Rate change failed:", response.status); // Handle errors
                }
            })
            .catch(error => {
                console.error('Error changing rate:', error);
            });
    }

    function resetRate() {
        fetch('/gametime/reset_rate', { method: 'POST' }) // Send POST to new route
            .then(response => {
                if (response.ok) {
                    console.log('rate has been reset')
                    updateTimeRate(); // Refresh display after resetting rate
                } else {
                    console.error("Error resetting rate:", response.status);
                }
            })
            .catch(error => {
                console.error("Error resetting rate:", error); // Handle errors
            });

    }

    
    ratePlusButton.addEventListener('click', () => updateRate(+1));
    ratePlusButton10.addEventListener('click', () => updateRate(+10));
    ratePlusButton100.addEventListener('click', () => updateRate(+100));
    ratePlusButton1000.addEventListener('click', () => updateRate(+1000));
    rateResetButton.addEventListener('click', resetRate); // Call resetRate function

});