from voice_input import listen_voice
from voice_output import speak
import reminders_manager as rm
import pywhatkit
import wikipedia
import webbrowser
from datetime import datetime
import config
import os
import time
import shutil
import pyautogui
import subprocess 
import psutil
import json
import email_manager as em
import smtplib
from ai_engine import ask_ai
import tray_manager
import threading
import voice_auth
import pin_auth
import security_state






AI_CONTEXT = []
MAX_CONTEXT = 5
WAITING_FOR_COMMAND = False
IDLE_THRESHOLD_SECONDS = 30
WAITING_FOR_PIN = False
PENDING_SECURE_ACTION = None


USAGE_LOG_FILE = "usage_log.json"

PENDING_HABIT_ACTION = None
LAST_USER_INTERACTION = time.time()

PENDING_EMAIL = None

#study module
WORKFLOWS = {
    "study": ["open notepad", "open browser"],
    "work": ["open browser"],
    "focus": ["minimise all"]
}


# File Function
BASE_DIR = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
if not os.path.exists(BASE_DIR):
    speak("Base directory not found")
    exit()

#reminders 



#System Major Responses
def lock_pc():
    speak("Locking the system")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def restart_pc():
    speak("Restarting the system")
    os.system("shutdown /r /t 5")

def shutdown_pc():
    speak("Shutting down the system")
    os.system("shutdown /s /t 5")

def list_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        print(proc.info)
    speak("Running processes listed on screen")

def kill_process(name):
    for proc in psutil.process_iter(['name']):
        if name.lower() in proc.info['name'].lower():
            proc.kill()
            speak(f"Process {name} terminated")
            return
    speak("Process not found")

def take_screenshot():
    file = "screenshot.png"
    pyautogui.screenshot(file)
    speak("Screenshot saved")
def minimise_all():
    pyautogui.hotkey("win", "d")
    speak("All windows minimised")




# time dealing

def greet():
    hour = datetime.now().hour
    if hour < 12:
        speak("Good morning, how can I help you")
    elif hour < 17:
        speak("Good afternoon, how can I help you")
    else:
        speak("Good evening, how can I help you")


def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")


def tell_date():
    today = datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")


def tell_day():
    day = datetime.now().strftime("%A")
    speak(f"Today is {day}")


# system things opening

def open_notepad():
    speak("Opening Notepad")
    os.system("notepad")


def open_calculator():
    speak("Opening Calculator")
    os.system("calc")

# computer checking

def cpu_usage():
    import psutil
    usage = psutil.cpu_percent(interval=1)
    speak(f"CPU usage is {usage} percent")


def ram_usage():
    import psutil
    ram = psutil.virtual_memory().percent
    speak(f"RAM usage is {ram} percent")


def battery_status():
    import psutil
    battery = psutil.sensors_battery()
    if battery:
        speak(f"Battery level is {battery.percent} percent")
    else:
        speak("Battery information not available")



# Searcing on web commands

def google_search(query):
    speak(f"Searching Google for {query}")
    pywhatkit.search(query)


def youtube_search(query):
    speak(f"Searching YouTube for {query}")
    pywhatkit.playonyt(query)


def wikipedia_search(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except Exception:
        speak("No Wikipedia result found")


def play_song(song):
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)

#folder commad 
def create_folder(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        os.mkdir(path)
        speak(f"Folder {name} created")
    else:
        speak("Folder already exists")

def list_files():
    files = os.listdir(BASE_DIR)
    if files:
        for f in files:
            print(f)
        speak("Files listed on screen")
    else:
        speak("Folder is empty")

def open_folder(name):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        os.startfile(path)
        speak(f"Opening folder {name}")
    else:
        speak("Folder not found")

def delete_file(name):
    path = os.path.join(BASE_DIR, name)
    if os.path.exists(path):
        os.remove(path)
        speak(f"File {name} deleted")
    else:
        speak("File not found")

def find_file(name):
    for root, dirs, files in os.walk(BASE_DIR):
        if name in files:
            speak(f"File found at {root}")
            return
    speak("File not found")

#reminders code function

#Morning tye

def morning_routine():
    speak("Good morning Dev")
    tell_time()
    speak("Opening your morning news")
    webbrowser.open("https://news.google.com")
    speak("Stay focused and make today productive")


def evening_routine():
    speak("Good evening Dev")
    tell_time()
    speak("You may want to wrap up your work")
    speak("Remember to rest well and recharge")

def execute_action(action):
    if action == "open notepad":
        open_notepad()
    elif action == "open browser":
        webbrowser.open("https://www.google.com")
    elif action == "minimise all":
        minimise_all()

def run_workflow(name):
    actions = WORKFLOWS.get(name)

    if not actions:
        speak("No such workflow found")
        return

    speak(f"Starting {name} workflow")

    for action in actions:
        execute_action(action)

#usage

def load_usage_log():
    if not os.path.exists(USAGE_LOG_FILE):
        return []
    try:
        with open(USAGE_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_usage_log(logs):
    with open(USAGE_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)




def log_command(command):
    logs = load_usage_log()
    hour = datetime.now().hour

    logs.append({
        "command": command,
        "hour": hour
    })

    save_usage_log(logs)

def analyze_habits():
    logs = load_usage_log()
    stats = {}

    for log in logs:
        command = log["command"]
        hour = log["hour"]
        key = (command, hour)

        if key in stats:
            stats[key] += 1
        else:
            stats[key] = 1

    return stats

def get_time_context():
    hour = datetime.now().hour

    if 5 <= hour <= 11:
        return "morning"
    elif 12 <= hour <= 16:
        return "afternoon"
    elif 17 <= hour <= 21:
        return "evening"
    else:
        return "night"



LAST_HABIT_SUGGESTION_TIME = {}

def habit_suggestions():
    habits = analyze_habits()
    current_hour = datetime.now().hour
    now = time.time()

    for (command, hour), count in habits.items():
        context = get_time_context()
        if hour != current_hour:
            continue

        # cooldown: once per hour per command
        last_time = LAST_HABIT_SUGGESTION_TIME.get(command, 0)
        if now - last_time < 10:
            continue

        if count >= 5:
            global PENDING_HABIT_ACTION
            PENDING_HABIT_ACTION = command

            speak(f"You often {command} in the {context}. Should I do it now?")
            LAST_HABIT_SUGGESTION_TIME[command] = now
            break

        elif count >= 3:
            speak(f"You usually {command} in the {context}")
            LAST_HABIT_SUGGESTION_TIME[command] = now
            break

def add_to_context(role, text):
    AI_CONTEXT.append(f"{role}: {text}")

    # keep memory small
    if len(AI_CONTEXT) > MAX_CONTEXT:
        AI_CONTEXT.pop(0)


def build_prompt(user_text):
    context_text = "\n".join(AI_CONTEXT)
    return f"{context_text}\nUser: {user_text}" if context_text else user_text

def go_to_sleep():
    global WAITING_FOR_COMMAND
    WAITING_FOR_COMMAND = False
    voice_auth.reset_session()
    print("[SYSTEM]: Jarvis sleeping.")



def clear_ai_context():
    AI_CONTEXT.clear()

def is_idle():
    return time.time() - LAST_USER_INTERACTION > IDLE_THRESHOLD_SECONDS





def main():
    global PENDING_HABIT_ACTION
    global PENDING_EMAIL   
    global WAITING_FOR_COMMAND   
    global WAITING_FOR_PIN

    speak(config.WAKE_MESSAGE)
    active = False



    
    # Loop for user is there
    while True:
        if not tray_manager.JARVIS_ACTIVE:
            time.sleep(1)
            continue
        
        rm.check_reminders(speak)
        if not security_state.LISTENING_ENABLED:
            time.sleep(0.5)
            continue

        text = listen_voice()

    # 🔕 alarm ping only when user is idle
        if not text:
            rm.alarm_idle_ping(speak)

    # 🔐 PRIORITY CONFIRMATION (no wake word needed)
        if text:
            text = text.lower()
            # 🔐 MIC PRIVACY CONTROLS (STEP 3)
            if "disable listening" in text:
                security_state.LISTENING_ENABLED = False
                speak("Listening disabled")
                continue

            if "enable listening" in text:
                security_state.LISTENING_ENABLED = True
                speak("Listening enabled")
                continue


            if "yes" in text and (PENDING_HABIT_ACTION or PENDING_EMAIL):
                # simulate active state
                active = True

        if not PENDING_HABIT_ACTION and not PENDING_EMAIL:
            habit_suggestions()

        
        if text:
            LAST_USER_INTERACTION = time.time()


        
        # if not heared hear it again
        if not text:
            time.sleep(0.5)
            continue
            
        text = text.lower().strip()# 🔐 HANDLE PIN INPUT FIRST
        if WAITING_FOR_PIN:
            pin = text.strip()

            if pin_auth.verify_pin(pin):
                speak("Access granted.")
                action, value = PENDING_SECURE_ACTION

                if action == "delete":
                    delete_file(value)
                elif action == "shutdown":
                    shutdown_pc()
                elif action == "restart":
                    restart_pc()
                elif action == "kill":
                    kill_process(value)
                elif action == "email":
                    # email send logic later
                    pass

            else:
                if pin_auth.is_locked():
                    speak("Too many attempts. Access locked for one minute.")
                else:
                    speak("Access denied.")

            WAITING_FOR_PIN = False
            PENDING_SECURE_ACTION = None
            active = False
            continue

        
        # exit to stop (ONLY ONE CHECK NEEDED - works anytime)
        if "exit" in text or "stop" in text or "goodbye" in text:
            speak(config.EXIT_MESSAGE)
            tray_manager.JARVIS_ACTIVE = False
            active = False
            WAITING_FOR_COMMAND = False
            voice_auth.reset_session()
            print("[SYSTEM]: JARVIS stopped. GUI still running.")
            continue


        # Say jarvis Wake up
# --- Wake word & activation gate ---
        if not active:
            # allow confirmation without wake word
            if "yes" in text and (PENDING_HABIT_ACTION or PENDING_EMAIL):
                active = True
            elif config.WAKE_WORD in text:
                # 🔐 Voice authentication
                owner = voice_auth.identify_speaker()

                if not owner:
                    speak("Unknown voice detected. Access denied.")
                    active = False
                    continue

                active = True
                WAITING_FOR_COMMAND = True
                print("[SYSTEM]: Wake word detected. Jarvis activated.")

                if not voice_auth.SESSION_GREETED:
                    speak(f"Welcome back {owner}")
                    voice_auth.SESSION_GREETED = True

                if text.strip() == config.WAKE_WORD:
                    continue


            elif not WAITING_FOR_COMMAND:
                continue

        # ✅ CONFIRMATION SHOULD BYPASS LENGTH FILTER
        if text == "yes" and (PENDING_HABIT_ACTION or PENDING_EMAIL):
            active = True

        
        # ignore very short inputs
        if len(text) < 3:
            continue
        
        # what user said
        if "hello" in text:
            print("Command detected: HELLO")
            greet()
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "time" in text:
            print("Command detected: TIME")
            tell_time()
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "date" in text:
            print("Command detected: DATE")
            tell_date()
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "day" in text:
            print("Command detected: DAY")
            tell_day()
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "open notepad" in text:
            open_notepad()
            log_command("open notepad")   
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "open calculator" in text or "open calc" in text:
            print("Command detected: OPEN CALCULATOR")
            open_calculator()
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "cpu" in text:
            print("Command detected: CPU USAGE")
            cpu_usage()
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "ram" in text or "memory" in text:
            print("Command detected: RAM USAGE")
            ram_usage()
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "battery" in text:
            print("Command detected: BATTERY STATUS")
            battery_status()
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "search google for" in text:
            print("Command detected: GOOGLE SEARCH")
            query = text.replace("search google for", "").strip()
            google_search(query)
            active = False
            clear_ai_context()
            go_to_sleep()



        elif "youtube search" in text:
            print("Command detected: YOUTUBE SEARCH")
            query = text.replace("youtube search", "").strip()
            youtube_search(query)
            active = False
            clear_ai_context()
            go_to_sleep()


            
        elif "wikipedia" in text:
            print("Command detected: WIKIPEDIA SEARCH")
            query = text.replace("wikipedia", "").strip()
            wikipedia_search(query)
            active = False
            clear_ai_context()
            go_to_sleep()



        elif "play song" in text:
            print("Command detected: PLAY SONG")
            song = text.replace("play song", "").strip()
            play_song(song)
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "create folder" in text:
            folder = text.replace("create folder", "").strip()
            create_folder(folder)
            active = False
            clear_ai_context()
            go_to_sleep()



        elif "list files" in text:
            list_files()
            active = False
            clear_ai_context()
            go_to_sleep()



        elif "open folder" in text:
            folder = text.replace("open folder", "").strip()
            open_folder(folder)
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "delete file" in text:
            if pin_auth.is_locked():
                speak("Access temporarily locked. Try later.")
                active = False
                continue

            speak("This action is protected. Please say your PIN.")
            WAITING_FOR_PIN = True
            PENDING_SECURE_ACTION = (
                "delete",
                text.replace("delete file", "").strip()
            )
            active = False




        elif "find file" in text:
            file = text.replace("find file", "").strip()
            find_file(file)
            active = False
            clear_ai_context()
            go_to_sleep()



        elif "lock pc" in text:
            lock_pc()
            active = False
            clear_ai_context()
            go_to_sleep()



        elif "restart pc" in text:
            speak("This action is protected. Please say your PIN.")
            WAITING_FOR_PIN = True
            PENDING_SECURE_ACTION = ("restart", None)
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "shutdown pc" in text:
            speak("This action is protected. Please say your PIN.")
            WAITING_FOR_PIN = True
            PENDING_SECURE_ACTION = ("shutdown", None)
            active = False


        elif "list processes" in text:
            list_processes()
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "kill process" in text:
            name = text.replace("kill process", "").strip()
            speak("This action is protected. Please say your PIN.")
            WAITING_FOR_PIN = True
            PENDING_SECURE_ACTION = ("kill", name)
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "take screenshot" in text:
            take_screenshot()
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "minimise all" in text:
            minimise_all()
            active = False
            clear_ai_context()
            go_to_sleep()

        
        elif (
        "remind me to" in text
        or "set alarm for" in text
        or "set the alarm for" in text
        or "daily alarm" in text
        or "set daily alarm for" in text
        or "every day alarm" in text
    ):
            reminder = rm.parse_reminder(text)

            if reminder:
                success = rm.add_reminder(reminder)

                if success:
                    if reminder.get("repeat") == "daily":
                        speak("Daily reminder set")
                    else:
                        speak("Reminder saved")
                else:
                    speak("This reminder already exists")
            else:
                speak("I could not understand the reminder")

            active = False
            clear_ai_context()
            go_to_sleep()

        elif "snooze" in text:
            words = text.split()
            minutes = 5  # default snooze

            for w in words:
                if w.isdigit():
                    minutes = int(w)
                    break

            success = rm.snooze_last(minutes)

            if success:
                speak(f"Snoozed for {minutes} minutes")
            else:
                speak("Nothing to snooze")

            active = False
            clear_ai_context()
            go_to_sleep()
        elif "stop alarm" in text or "dismiss alarm" in text:
            if rm.stop_alarm():
                speak("Alarm stopped")
            else:
                speak("No active alarm")
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "list reminders" in text:
            reminders = rm.load_reminders()
            if not reminders:
                speak("No reminders set")
            for r in reminders:
                speak(f"{r['task']} at {r['time']}")
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "morning routine" in text:
            morning_routine()
            log_command("morning routine")
            active = False
            clear_ai_context()
            go_to_sleep()


        elif "evening routine" in text:
            evening_routine()
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "start" in text:
            workflow_name = text.replace("start", "").strip()
            run_workflow(workflow_name)
            active = False
            clear_ai_context()
            go_to_sleep()

        elif "send email" in text:
                    speak("This action is protected. Please say your PIN.")
                    WAITING_FOR_PIN = True
                    PENDING_SECURE_ACTION = ("email", None)
                    active = False

                    # demo email (can be improved later)
                    to_name = "me"
                    subject = "Test Email from Jarvis"
                    body = "Hello Dev, this is a test email sent by Jarvis."

                    msg = em.send_email(to_name, subject, body, speak)

                    if msg:
                        PENDING_EMAIL = msg
                        speak("I have prepared the email. Say yes to send it.")

                    active = False
                    WAITING_FOR_COMMAND = False


        elif "yes" in text:
            # 1️⃣ Habit confirmation
            if PENDING_HABIT_ACTION:
                action = PENDING_HABIT_ACTION
                PENDING_HABIT_ACTION = None

                if action == "open notepad":
                    open_notepad()
                elif action == "open browser":
                    webbrowser.open("https://www.google.com")
                elif action == "minimise all":
                    minimise_all()
                else:
                    speak("I know this habit, but I cannot execute it yet")

                active = False
                WAITING_FOR_COMMAND = False

            # 2️⃣ Email confirmation
            elif PENDING_EMAIL:
                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()

                    # replace later with real credentials
                    server.login("charayadev11@gmail.com", "cfli dshh pktd eltk")

                    server.send_message(PENDING_EMAIL)
                    server.quit()

                    speak("Email sent successfully")

                except Exception:
                    speak("I could not send the email")

                PENDING_EMAIL = None
                active = False
                WAITING_FOR_COMMAND = False
            

            else:
                speak("There is nothing to confirm")
                active = False
                WAITING_FOR_COMMAND=False

        

           
            # prevent junk AI calls
            if len(text.split()) < 2:
                speak("Please say a complete question.")
                active = False
                continue

            print("[AI]: Processing request")


            prompt = build_prompt(text)
            ai_reply = ask_ai(prompt, idle=is_idle())

        
            if ai_reply:
                speak(ai_reply)

                add_to_context("User", text)
                add_to_context("AI", ai_reply)
                clear_ai_context()

            else:
                speak("Sorry, I don't have an answer for that.")

            active = False
            go_to_sleep()


        
        time.sleep(0.5)


if __name__ == "__main__":
    import gui_dashboard
    import threading

    if __name__ == "__main__":
        # Start JARVIS brain (background)
        threading.Thread(target=main, daemon=True).start()

        # Start GUI (main thread)
        gui_dashboard.start_gui()