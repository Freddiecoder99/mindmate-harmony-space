const API_URL = 'http://localhost:5000/api';

export async function trackMood(mood, situation) {
    try {
        const response = await fetch(`${API_URL}/track-mood`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mood, situation })
        });
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

export async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
