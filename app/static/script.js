// Above this percentage a resource is treated as under pressure and the header
// badge turns amber. Same warning level used in the Grafana panels.
const PRESSURE_THRESHOLD = 85;

function setStatus(colour, text) {
    document
        .getElementById("status-badge")
        .style.setProperty("--status", `var(--${colour})`);

    document.getElementById("status-text").textContent = text;
}

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

        const underPressure = [data.cpu, data.memory, data.disk].some(
            (value) => value >= PRESSURE_THRESHOLD
        );

        setStatus(underPressure ? "warning" : "healthy",
                  underPressure ? "Degraded" : "Healthy");
    } catch (error) {
        // If the backend cannot be reached, say so. A dashboard that still
        // shows green when it has no data is worse than no dashboard.
        console.error(error);
        setStatus("danger", "Unreachable");
    }
}

updateDashboard();
setInterval(updateDashboard, 5000);
