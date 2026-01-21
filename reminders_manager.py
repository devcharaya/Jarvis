import json
from datetime import datetime
from datetime import datetime, timedelta
import os

IDLE_PING_COUNT = 0
ALARM_ACTIVE = False


LAST_TRIGGERED_INDEX = None
LAST_TRIGGERED_MINUTE = None

REMINDER_FILE = "reminders.json"

def popup(message):
    import ctypes
    ctypes.windll.user32.MessageBoxW(
        0,
        message,
        "Jarvis Alert",
        1
    )


def system_beep():
    try:
        # Windows beep
        import winsound
        winsound.Beep(1000, 800)
    except:
        # Fallback (console bell)
        print("\a")


def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []

    try:
       with open(REMINDER_FILE, "r") as f:
        return json.load(f)


    except Exception:
        return []


def save_reminders(reminders):
    data = json.dumps(reminders)
    with open(REMINDER_FILE, "w") as f:
     json.dump(reminders, f, indent=2)



def convert_to_24hr(time_str):
    time_str = time_str.lower().replace(".", "").strip()

    # supported:
    # 11 am
    # 11:00 am
    # 7 pm
    # 7:30 pm

    if "am" in time_str or "pm" in time_str:
        period = "am" if "am" in time_str else "pm"
        time_part = time_str.replace("am", "").replace("pm", "").strip()

        if ":" in time_part:
            hour, minute = map(int, time_part.split(":"))
        else:
            hour = int(time_part)
            minute = 0

        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0

        return f"{hour:02d}:{minute:02d}"

    return None


def parse_reminder(command):
    command = command.lower()
    if (
        "daily alarm" in command
        or "set daily alarm for" in command
        or "every day alarm" in command
    ):
        if "for" in command:
            if (
                "daily alarm" in command
                or "set daily alarm for" in command
                or "every day alarm" in command
            ):
                if "for" in command:
                    time_part = command.split("for")[-1].strip()
                elif " at " in command:
                    time_part = command.split(" at ")[-1].strip()
                else:
                    return None

                time_24 = convert_to_24hr(time_part)

                if not time_24:
                    return None

                return {
                    "task": "wake up",
                    "time": time_24,
                    "type": "alarm",
                    "triggered": False,
                    "repeat": "daily",
                    "snoozed_until": None
                }
        elif " at " in command:
            time_part = command.split(" at ")[-1].strip()
        else:
            return None
        time_24 = convert_to_24hr(time_part)

        if not time_24:
            return None

        return {
            "task": "wake up",
            "time": time_24,
            "type": "alarm",
            "triggered": False,
            "repeat": "daily",
            "snoozed_until": None
        }
    if "set alarm for" in command or "set the alarm for" in command:
        time_part = command.split("for")[-1].strip()
        time_24 = convert_to_24hr(time_part)

        if not time_24:
            return None

        return {
            "task": "wake up",
            "time": time_24,
            "type": "alarm",
            "triggered": False,
            "repeat": None,
            "snoozed_until": None
        }
    
    if "every day" in command and " at " in command:
        time_part = command.split(" at ")[-1]
        time_24 = convert_to_24hr(time_part)

        if not time_24:
            return None

        return {
            "task": "daily reminder",
            "time": time_24,
            "type": "reminder",
            "triggered": False,
            "repeat": "daily",
            "snoozed_until": None
        }

    if "remind me to" in command and " at " in command:
        task_part = command.split("remind me to")[1]
        task, time_part = task_part.rsplit(" at ", 1)

        time_24 = convert_to_24hr(time_part)
        if not time_24:
            return None

        return {
            "task": task.strip(),
            "time": time_24,
            "type": "reminder",
            "triggered": False,
            "repeat": None,
            "snoozed_until": None
        }

    return None
def parse_reminder(command):
    command = command.lower()

    # 1️⃣ DAILY REMINDER (every day at)
    if "every day" in command and " at " in command:
        time_part = command.split(" at ")[-1].strip()
        time_24 = convert_to_24hr(time_part)

        if not time_24:
            return None

        return {
            "task": "daily reminder",
            "time": time_24,
            "type": "reminder",
            "triggered": False,
            "repeat": "daily",
            "snoozed_until": None
        }

    # 2️⃣ DAILY ALARM
    if (
        "daily alarm" in command
        or "set daily alarm for" in command
        or "every day alarm" in command
    ):
        if "for" in command:
            time_part = command.split("for")[-1].strip()
        elif " at " in command:
            time_part = command.split(" at ")[-1].strip()
        else:
            return None

        time_24 = convert_to_24hr(time_part)
        if not time_24:
            return None

        return {
            "task": "wake up",
            "time": time_24,
            "type": "alarm",
            "triggered": False,
            "repeat": "daily",
            "snoozed_until": None
        }

    # 3️⃣ NORMAL ALARM
    if "set alarm for" in command or "set the alarm for" in command:
        time_part = command.split("for")[-1].strip()
        time_24 = convert_to_24hr(time_part)

        if not time_24:
            return None

        return {
            "task": "wake up",
            "time": time_24,
            "type": "alarm",
            "triggered": False,
            "repeat": None,
            "snoozed_until": None
        }

    # 4️⃣ NORMAL REMINDER
    if "remind me to" in command and " at " in command:
        task_part = command.split("remind me to")[1]
        task, time_part = task_part.rsplit(" at ", 1)

        time_24 = convert_to_24hr(time_part)
        if not time_24:
            return None

        return {
            "task": task.strip(),
            "time": time_24,
            "type": "reminder",
            "triggered": False,
            "repeat": None,
            "snoozed_until": None
        }

    return None

def stop_alarm():
    global ALARM_ACTIVE, IDLE_PING_COUNT
    if ALARM_ACTIVE:
        ALARM_ACTIVE = False
        IDLE_PING_COUNT = 0
        return True
    return False


def alarm_idle_ping(speak):
    global ALARM_ACTIVE, IDLE_PING_COUNT

    if ALARM_ACTIVE:
        IDLE_PING_COUNT += 1
        system_beep()

        if IDLE_PING_COUNT >= 3:
            print("⚠️⚠️⚠️ PLEASE RESPOND ⚠️⚠️⚠️")
            speak("Please respond. Alarm is still active.")
        else:
            speak("Alarm still active")



def add_reminder(reminder):
    reminders = load_reminders()

    for r in reminders:
        if (
            r["task"] == reminder["task"]
            and r["time"] == reminder["time"]
            and r["type"] == reminder["type"]
        ):
            return False  # duplicate found

    reminders.append(reminder)
    save_reminders(reminders)
    return True


def check_reminders(speak):
    global LAST_TRIGGERED_INDEX, LAST_TRIGGERED_MINUTE

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_minute = now.strftime("%Y-%m-%d %H:%M")

    if LAST_TRIGGERED_MINUTE == current_minute:
        return

    reminders = load_reminders()
    updated = False
    triggered_now = False

    for index, reminder in enumerate(reminders):
        if not reminder["triggered"] and reminder["time"] == current_time:
            if reminder["type"] == "alarm":
                global ALARM_ACTIVE

                if reminder["type"] == "alarm":
                    ALARM_ACTIVE = True
                    print("\n" + "🚨" * 15)
                    print("🚨🚨🚨 ALARM ACTIVE 🚨🚨🚨")
                    print(f"⏰ {reminder['task']}")
                    print("🚨" * 15 + "\n")


                    system_beep()
                    speak(f"Alarm! {reminder['task']}")
                    popup(f"Alarm: {reminder['task']}")

                else:
                    print("\n🔔 REMINDER 🔔")
                    print(f"👉 {reminder['task']}\n")
                    system_beep()
                    speak(f"Reminder: {reminder['task']}")
            else:
                speak(f"Reminder: {reminder['task']}")

            if reminder.get("repeat") == "daily":
                next_day = datetime.now() + timedelta(days=1)
                reminder["time"] = next_day.strftime("%H:%M")
                reminder["triggered"] = False
            else:
                reminder["triggered"] = True
            LAST_TRIGGERED_INDEX = index
            triggered_now = True
            updated = True

    if triggered_now:
        LAST_TRIGGERED_MINUTE = current_minute

    if updated:
        save_reminders(reminders)

def snooze_last(minutes):
    global LAST_TRIGGERED_INDEX

    if LAST_TRIGGERED_INDEX is None:
        return False

    reminders = load_reminders()
    reminder = reminders[LAST_TRIGGERED_INDEX]

    now = datetime.now()
    snoozed_time = now + timedelta(minutes=minutes)

    reminder["time"] = snoozed_time.strftime("%H:%M")
    reminder["triggered"] = False
    reminder["snoozed_until"] = reminder["time"]

    save_reminders(reminders)
    return True



