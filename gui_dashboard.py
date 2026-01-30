import tkinter as tk
import psutil
import json
import os
from datetime import datetime
import os
import pyautogui
import threading
import tray_manager
import security_state
import pin_auth




SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "voice_enabled": True,
    "ai_enabled": True,
    "ai_response_length": 60,
    "ai_cooldown": 5,
    "default_workflow": "study"
}



def enable_listening():
    security_state.LISTENING_ENABLED = True



def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception:
        pass


REFRESH_INTERVAL = 2000  # milliseconds (2 seconds)
LOG_REFRESH_INTERVAL = 4000  # 4 seconds
USAGE_LOG_FILE = "usage_log.json"



def start_gui():
    root = tk.Tk()

    def reopen_gui():
        root.deiconify()
        root.lift()
        root.focus_force()

    tray_manager.GUI_CALLBACK = reopen_gui


    # Window setup
    root.title("JARVIS Dashboard")
    root.geometry("800x700")
    root.resizable(False, False)
    root.configure(bg="#1e1e1e")
    
    
    settings = load_settings()



    # -------------------------
    # QUICK ACTION FUNCTIONS
    # -------------------------
    def lock_pc_action():
        os.system("rundll32.exe user32.dll,LockWorkStation")

    def screenshot_action():
        pyautogui.screenshot("screenshot.png")


    # -------------------------
    # LEFT PANEL — JARVIS STATUS
    # -------------------------
    left_frame = tk.Frame(root, bg="#252526", width=400, height=500)
    left_frame.pack(side="left", fill="y")

    tk.Label(
        left_frame,
        text="JARVIS STATUS",
        fg="white",
        bg="#252526",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=20)

    jarvis_status_label = tk.Label(
        left_frame,
        text="Status: Sleeping",
        fg="lightgreen",
        bg="#252526",
        font=("Segoe UI", 11)
    )
    jarvis_status_label.pack(pady=10)

    def update_jarvis_status():
            if tray_manager.JARVIS_ACTIVE:
                jarvis_status_label.config(text="Status: Active", fg="lightgreen")
            else:
                jarvis_status_label.config(text="Status: Paused", fg="orange")

            root.after(500, update_jarvis_status)
       



    voice_status_label = tk.Label(
        left_frame,
        text="Voice: Enabled",
        fg="white",
        bg="#252526",
        font=("Segoe UI", 11)
    )
    voice_status_label.pack(pady=10)

    ai_status_label = tk.Label(
        left_frame,
        text="AI: Offline",
        fg="orange",
        bg="#252526",
        font=("Segoe UI", 11)
    )
    ai_status_label.pack(pady=10)

    security_label = tk.Label(
    left_frame,
    text="Security: Secure",
    fg="lightgreen",
    bg="#252526",
    font=("Segoe UI", 11)
    )
    security_label.pack(pady=10)


    # -------------------------
    # QUICK ACTION BUTTONS
    # -------------------------
    tk.Button(
        left_frame,
        text="🔒 Lock PC",
        width=20,
        bg="#333333",
        fg="white",
        command=lock_pc_action
    ).pack(pady=10)

    tk.Button(
        left_frame,
        text="📸 Screenshot",
        width=20,
        bg="#333333",
        fg="white",
        command=screenshot_action
    ).pack(pady=5)

    tk.Button(
    left_frame,
    text="🎤 Enable Listening",
    width=20,
    bg="#007acc",
    fg="white",
    command=enable_listening
   ).pack(pady=10)


    # -------------------------
    # RIGHT PANEL — SYSTEM STATS
    # -------------------------
    right_frame = tk.Frame(root, bg="#1e1e1e", width=400, height=500)
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(
        right_frame,
        text="SYSTEM STATS",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=20)

    cpu_label = tk.Label(
        right_frame,
        text="CPU: -- %",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 11)
    )
    cpu_label.pack(pady=10)

    ram_label = tk.Label(
        right_frame,
        text="RAM: -- %",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 11)
    )
    ram_label.pack(pady=10)

    battery_label = tk.Label(
        right_frame,
        text="Battery: -- %",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 11)
    )
    battery_label.pack(pady=10)


    # -------------------------
    # COMMAND HISTORY PANEL
    # -------------------------
    history_frame = tk.Frame(root, bg="#1e1e1e", height=150)
    history_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(
        history_frame,
        text="COMMAND HISTORY",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")

    history_text = tk.Text(
        history_frame,
        height=6,
        bg="#111111",
        fg="white",
        insertbackground="white",
        state="disabled"
    )
    history_text.pack(fill="x", pady=5)


    # -------------------------
    # SYSTEM LOG PANEL
    # -------------------------
    log_frame = tk.Frame(root, bg="#1e1e1e", height=150)
    log_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(
        log_frame,
        text="SYSTEM LOGS",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")

    log_text = tk.Text(
        log_frame,
        height=5,
        bg="#111111",
        fg="gray",
        insertbackground="white",
        state="disabled"
    )
    log_text.pack(fill="x", pady=5)
        

    # -------------------------
    # SETTINGS PANEL
    # -------------------------
    settings_frame = tk.Frame(root, bg="#1e1e1e")
    settings_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(
        settings_frame,
        text="SETTINGS",
        fg="white",
        bg="#1e1e1e",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w")

         # --- AI Response Length ---
    tk.Label(
        settings_frame,
        text="AI Response Length",
        fg="white",
        bg="#1e1e1e"
    ).pack(anchor="w", pady=(10, 0))

    def on_response_len(val):
        settings["ai_response_length"] = int(float(val))
        save_settings(settings)

    response_slider = tk.Scale(
        settings_frame,
        from_=20,
        to=150,
        orient="horizontal",
        command=on_response_len,
        bg="#1e1e1e",
        fg="white",
        highlightthickness=0
    )
    response_slider.set(settings["ai_response_length"])
    response_slider.pack(anchor="w")

    # --- AI Cooldown ---
    tk.Label(
        settings_frame,
        text="AI Cooldown (seconds)",
        fg="white",
        bg="#1e1e1e"
    ).pack(anchor="w", pady=(10, 0))

    def on_cooldown(val):
        settings["ai_cooldown"] = int(float(val))
        save_settings(settings)

    cooldown_slider = tk.Scale(
        settings_frame,
        from_=1,
        to=15,
        orient="horizontal",
        command=on_cooldown,
        bg="#1e1e1e",
        fg="white",
        highlightthickness=0
    )
    cooldown_slider.set(settings["ai_cooldown"])
    cooldown_slider.pack(anchor="w")

    # --- Default Workflow ---
    tk.Label(
        settings_frame,
        text="Default Workflow",
        fg="white",
        bg="#1e1e1e"
    ).pack(anchor="w", pady=(10, 0))

    workflow_var = tk.StringVar(value=settings["default_workflow"])

    def on_workflow_change(*_):
        settings["default_workflow"] = workflow_var.get()
        save_settings(settings)

    workflow_menu = tk.OptionMenu(
        settings_frame,
        workflow_var,
        "study",
        "work",
        "focus"
    )
    workflow_menu.config(bg="#333333", fg="white")
    workflow_menu.pack(anchor="w")

    workflow_var.trace_add("write", on_workflow_change)




    # --- Toggles ---
    voice_var = tk.BooleanVar(value=settings["voice_enabled"])
    ai_var = tk.BooleanVar(value=settings["ai_enabled"])

    def on_toggle():
        settings["voice_enabled"] = voice_var.get()
        settings["ai_enabled"] = ai_var.get()
        save_settings(settings)

    tk.Checkbutton(
        settings_frame,
        text="Voice Enabled",
        variable=voice_var,
        command=on_toggle,
        bg="#1e1e1e",
        fg="white",
        selectcolor="#333333"
    ).pack(anchor="w")

    tk.Checkbutton(
        settings_frame,
        text="AI Enabled",
        variable=ai_var,
        command=on_toggle,
        bg="#1e1e1e",
        fg="white",
        selectcolor="#333333"
    ).pack(anchor="w")
    
    def update_voice_status():
        if security_state.LISTENING_ENABLED:
            voice_status_label.config(text="Voice: Enabled", fg="lightgreen")
        else:
            voice_status_label.config(text="Voice: Disabled", fg="red")

        root.after(500, update_voice_status)
   
   
    update_voice_status()
    update_jarvis_status()



 



    # -------------------------
    # UPDATE FUNCTION
    # -------------------------
    def update_system_stats():
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()

        cpu_label.config(text=f"CPU: {cpu} %")
        ram_label.config(text=f"RAM: {ram} %")

        if battery:
            battery_label.config(text=f"Battery: {battery.percent} %")
        else:
            battery_label.config(text="Battery: N/A")

        # schedule next update
        root.after(REFRESH_INTERVAL, update_system_stats)

    update_system_stats()

    def update_security_status():
        if pin_auth.is_locked():
            security_label.config(text="Security: PIN Locked 🔒", fg="red")
        else:
            security_label.config(text="Security: Secure", fg="lightgreen")

        root.after(1000, update_security_status)
   
    update_security_status()
    

    
    def update_command_history():
        if not os.path.exists(USAGE_LOG_FILE):
            return

        try:
            with open(USAGE_LOG_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            return

        last_entries = data[-5:]  # show last 5 commands

        history_text.config(state="normal")
        history_text.delete("1.0", tk.END)

        for entry in last_entries:
            hour = entry.get("hour", "--")
            cmd = entry.get("command", "")
            history_text.insert(tk.END, f"{hour}:00 → {cmd}\n")

        history_text.config(state="disabled")

        root.after(LOG_REFRESH_INTERVAL, update_command_history)
    def update_system_logs():
        log_text.config(state="normal")
        log_text.delete("1.0", tk.END)

        log_text.insert(tk.END, "System running normally\n")
        log_text.insert(tk.END, "No critical alerts\n")

        log_text.config(state="disabled")

        root.after(LOG_REFRESH_INTERVAL, update_system_logs)

    update_system_stats()
    update_command_history()
    update_system_logs()




    def on_close():
        root.withdraw()
        threading.Thread(target=tray_manager.run_tray, daemon=True).start()



    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    
if __name__ == "__main__":
    start_gui()
