let selectedMachine = null;

async function loadMachines() {
    try {
        const res = await fetch("http://localhost:5000/api/get_machines");
        const machines = await res.json();

        const container = document.getElementById("machines-container");
        container.innerHTML = "";

        machines.forEach(machine => {
            const btn = document.createElement("button");
            btn.textContent = machine;
            btn.onclick = () => showLogsPage(machine);
            container.appendChild(btn);
        });
    } catch (err) {
        console.error("Error loading machines:", err);
    }
}

function showLogsPage(machine) {
    selectedMachine = machine;
    document.getElementById("machines-page").style.display = "none";
    document.getElementById("logs-page").style.display = "block";
    document.getElementById("selected-machine").textContent = `מחשב נבחר: ${machine}`;
}

document.getElementById("back-btn").onclick = () => {
    document.getElementById("logs-page").style.display = "none";
    document.getElementById("machines-page").style.display = "block";
};

document.getElementById("fetch-logs-btn").onclick = async () => {
    if (!selectedMachine) return;

    const date = document.getElementById("date-input").value;
    const time = document.getElementById("time-input").value;

    try {
        const url = `http://localhost:5000/api/get_logs?machine=${selectedMachine}&date=${date}&time=${time}`;
        const res = await fetch(url);
        const data = await res.json();

        const container = document.getElementById("logs-container");
        container.innerHTML = "";

        if (data.logs && data.logs.length > 0) {
            const logDiv = document.createElement("div");
            logDiv.className = "log";
            logDiv.textContent = data.logs;
            container.appendChild(logDiv);
        } else {
            container.textContent = "אין לוגים להצגה.";
        }
    } catch (err) {
        console.error("Error loading logs:", err);
    }
};

// טען את רשימת המחשבים בהתחלה
loadMachines();
