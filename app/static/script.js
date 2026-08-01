async function updateDashboard() {
    try {
        const response = await fetch("/metrics-data");

        if (!response.ok) {
            throw new Error("Could not load system metrics.");
        }

        const data = await response.json();

        document.getElementById("cpu-value").textContent = `${data.cpu}%`;
        document.getElementById("memory-value").textContent = `${data.memory}%`;
        document.getElementById("disk-value").textContent = `${data.disk}%`;

        document.getElementById("uptime-value").textContent = data.uptime;
        document.getElementById("version-value").textContent = `v${data.version}`;
        document.getElementById("last-updated").textContent = new Date().toLocaleTimeString();
    } catch (error) {
        console.error(error);
    }
}

updateDashboard();
setInterval(updateDashboard, 5000);