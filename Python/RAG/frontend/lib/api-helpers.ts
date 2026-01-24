export async function fetchOllamaModels() {
    try {
        const response = await fetch("http://127.0.0.1:8000/ollama/localmodels", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-store'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        // data is now: [{model: "...", parameter_size: "..."}, ...]
        return data; 
    } catch (error) {
        console.error("Could not fetch models:", error);
        // CHANGE: Return an empty array so models.map() doesn't break
        return []; 
    }
}

