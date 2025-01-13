import { updateGameTime } from './gametime.js';


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
                    updateGameTime(); // Immediately refresh the display after successful change
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
                    updateGameTime(); // Refresh display after resetting rate
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