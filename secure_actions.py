import os
import psutil
from voice_output import speak

BASE_DIR = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")

def delete_file(name):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        os.remove(path)
        speak(f"File {name} deleted")
    else:
        speak("File not found")

def shutdown_pc():
    speak("Shutting down the system")
    os.system("shutdown /s /t 5")

def restart_pc():
    speak("Restarting the system")
    os.system("shutdown /r /t 5")

def kill_process(name):
    for proc in psutil.process_iter(['name']):
        if name.lower() in proc.info['name'].lower():
            proc.kill()
            speak(f"Process {name} terminated")
            return
    speak("Process not found")
def execute_secure_action(action, value=None):
    if action == "delete":
        delete_file(value)

    elif action == "shutdown":
        shutdown_pc()

    elif action == "restart":
        restart_pc()

    elif action == "kill":
        kill_process(value)

    else:
        speak("Unknown secure action")
