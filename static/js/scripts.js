document.getElementById('get-recommendations').addEventListener('click', async () => {
    const country = document.getElementById('country').value;
    const season = document.getElementById('season').value;

    const statusMessage = document.getElementById('status-message');
    const recommendationsDiv = document.getElementById('recommendations');

    statusMessage.textContent = 'Fetching recommendations...';
    recommendationsDiv.textContent = '';

    try {
        const response = await fetch(`/recommendations/?country=${country}&season=${season}`);
        const data = await response.json();
        const uid = data.uid;

        let isPending = true;
        while (isPending) {
            const statusResponse = await fetch(`/status/${uid}`);
            const statusData = await statusResponse.json();

            if (statusResponse.status === 404) {
                statusMessage.textContent = 'Error: UID not found.';
                isPending = false;
            } else if (statusData.status === 'pending') {
                statusMessage.textContent = 'Recommendations are not yet available. Please try again later.';
                await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds before checking again
            } else if (statusData.status === 'completed') {
                statusMessage.textContent = 'Recommendations:';
                recommendationsDiv.innerHTML = `<ul>${statusData.recommendations.map(rec => `<li>${rec}</li>`).join('')}</ul>`;
                isPending = false;
            }
        }
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        statusMessage.textContent = 'An error occurred while fetching recommendations.';
    }
});
