const API_BASE = "http://localhost:5000/api";
let selectedMachine = null;

// ====== מניעת רענון דף אוטומטי ======
window.addEventListener('beforeunload', function(e) {
  e.preventDefault();
  e.returnValue = '';
});

// חסימת כל סוגי הרענון
(function() {
  const originalReload = location.reload;
  location.reload = function() {
    console.log("רענון דף נחסם!");
    return false;
  };
  
  const metaElements = document.querySelectorAll('meta[http-equiv="refresh"]');
  metaElements.forEach(meta => meta.remove());
  
  window.addEventListener('popstate', function(e) {
    e.preventDefault();
  });
})();

// ====== טעינת רשימת המחשבים ======
async function loadMachines() {
  try {
    const res = await fetch(`${API_BASE}/machines`);
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
    console.error("שגיאה בטעינת מחשבים:", err);
  }
}

// ====== מעבר למסך לוגים וטעינת תאריכים ======
async function showLogsPage(machine) {
  selectedMachine = machine;
  document.getElementById("machines-page").style.display = "none";
  document.getElementById("logs-page").style.display = "block";
  document.getElementById("selected-machine").textContent = `מחשב נבחר: ${machine}`;

  document.getElementById("logs-container").innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/machines/${machine}/dates`);
    const dates = await res.json();

    if (!Array.isArray(dates)) {
      console.error("Server returned an error:", dates);
      return;
    }

    const dateSelect = document.getElementById("date-select");
    dateSelect.innerHTML = "";
    dateSelect.addEventListener("change", () => populateHourSelect(dateSelect.value));

    dates.forEach(date => {
      const option = document.createElement("option");
      option.value = date;
      option.textContent = date;
      dateSelect.appendChild(option);
    });

    if (dates.length > 0) populateHourSelect(dates[0]);

  } catch (err) {
    console.error("שגיאה בטעינת תאריכים:", err);
  }
}

// ====== חזרה למסך הראשי ======
document.getElementById("back-btn").onclick = () => {
  document.getElementById("logs-page").style.display = "none";
  document.getElementById("machines-page").style.display = "block";
  document.getElementById("logs-container").innerHTML = "";
};

// ====== טעינת שעות לפי תאריך ======
async function populateHourSelect(date) {
  if (!selectedMachine || !date) return;

  try {
    const res = await fetch(`${API_BASE}/machines/${selectedMachine}/dates/${date}/hours`);
    const hours = await res.json();

    const hourSelect = document.getElementById("hour-select");
    hourSelect.innerHTML = "";

    hours.forEach(hh => {
      const option = document.createElement("option");
      option.value = hh;
      option.textContent = hh;
      hourSelect.appendChild(option);
    });
  } catch (err) {
    console.error("שגיאה בטעינת שעות:", err);
  }
}

// ====== הצגת לוגים לפי שעה ======
function displayLogs(logsData, hour) {
  const container = document.getElementById("logs-container");
  container.innerHTML = "";

  if (!logsData || logsData.length === 0) {
    container.textContent = "אין לוגים להצגה.";
    return;
  }

  const logEntries = logsData.join('\n').split('==================================================');

  const filteredLogs = logEntries.filter(entry => {
    const trimmedEntry = entry.trim();
    if (!trimmedEntry) return false;

    const match = trimmedEntry.match(/^\[\d{4}-\d{2}-\d{2} (\d{2}):\d{2}:\d{2}\]/);
    return match && match[1] === hour;
  });

  filteredLogs.forEach(entry => {
    const trimmedEntry = entry.trim();
    const lines = trimmedEntry.split('\n');
    const firstLine = lines[0];

    const timeMatch = firstLine.match(/^\[\d{4}-\d{2}-\d{2} (\d{2}:\d{2}:\d{2})\]/);
    if (timeMatch) {
      const timeOnly = timeMatch[1];
      const content = lines.slice(1).join('\n').trim();

      const logDiv = document.createElement("div");
      logDiv.className = "log";
      logDiv.style.whiteSpace = "pre-wrap";
      logDiv.style.marginBottom = "15px";
      logDiv.style.borderBottom = "1px solid #ddd";
      logDiv.style.paddingBottom = "10px";
      logDiv.textContent = `${timeOnly} - ${content}`;
      container.appendChild(logDiv);
    }
  });

  if (filteredLogs.length === 0) {
    container.textContent = "אין לוגים לשעה זו.";
  }
}

// ====== טעינת לוגים לפי שעה ======
document.getElementById("fetch-logs-btn").onclick = async () => {
  if (!selectedMachine) return;

  const date = document.getElementById("date-select").value;
  const hour = document.getElementById("hour-select").value;
  if (!date || !hour) return;

  try {
    const res = await fetch(`${API_BASE}/machines/${selectedMachine}/logs?date=${date}`);
    const data = await res.json();

    displayLogs(data.logs, hour);
  } catch (err) {
    console.error("שגיאה בטעינת לוגים:", err);
  }
};

// ====== טעינה ראשונית של מכונות ======
window.addEventListener('DOMContentLoaded', () => {
  loadMachines();
});
