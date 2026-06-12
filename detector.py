# detector.py — Smart Privacy Shield backend
from pynput import keyboard
import psutil
import datetime
import json

log = []  # stores detected events

def check_suspicious_processes():
    """Scans running processes and flags keyboard-related ones"""
    suspicious = []
    # These are libraries/tools known to do keyboard monitoring
    keywords = ['pynput', 'pyHook', 'keylogger', 'evtest', 'xinput']
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            name = proc.info['name'].lower()
            for kw in keywords:
                if kw in cmdline or kw in name:
                    suspicious.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'risk': 'HIGH'
                    })
        except:
            pass  # some processes are protected, skip them
    return suspicious

def log_event(message, level="INFO"):
    """Adds a timestamped event to our log"""
    entry = {
        'time': datetime.datetime.now().strftime("%H:%M:%S"),
        'level': level,
        'message': message
    }
    log.append(entry)
    print(f"[{entry['time']}] [{level}] {message}")

# Run a quick scan when the script starts
log_event("Smart Privacy Shield started")
found = check_suspicious_processes()
if found:
    for p in found:
        log_event(f"Suspicious process found: {p['name']} (PID {p['pid']})", "WARNING")
else:
    log_event("No suspicious processes detected — system clean", "OK")

# Save results to a JSON file the dashboard can read
with open('scan_results.json', 'w') as f:
    json.dump({'events': log, 'processes': found}, f, indent=2)

print("\nDone! Results saved to scan_results.json")