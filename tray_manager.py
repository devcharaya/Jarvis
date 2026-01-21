import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys
import os
import security_state


GUI_CALLBACK = None
TRAY_RUNNING = False


# Shared state flags
JARVIS_ACTIVE = True
GUI_VISIBLE = True


def create_icon(active=True):
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)

    color = "green" if active else "gray"
    draw.ellipse((16, 16, 48, 48), fill=color)

    return image


def on_open_dashboard(icon, _):
    if GUI_CALLBACK:
        GUI_CALLBACK()


def on_pause_jarvis(icon, _):
    global JARVIS_ACTIVE

    if JARVIS_ACTIVE:
        # Pause JARVIS
        JARVIS_ACTIVE = False
        security_state.LISTENING_ENABLED = False
        icon.icon = create_icon(False)
    else:
        # Resume JARVIS
        JARVIS_ACTIVE = True
        security_state.LISTENING_ENABLED = True
        icon.icon = create_icon(True)



def on_exit(icon, _):
    icon.stop()
    os._exit(0)


def get_pause_title(icon):
    return "Pause JARVIS" if JARVIS_ACTIVE else "Resume JARVIS"


def run_tray():
    global TRAY_RUNNING
    if TRAY_RUNNING:
        return

    TRAY_RUNNING = True

    menu = (
        item("Open Dashboard", on_open_dashboard),
        item(get_pause_title, on_pause_jarvis),
        item("Exit", on_exit)
    )

    icon = pystray.Icon(
        "JARVIS",
        create_icon(JARVIS_ACTIVE),
        "JARVIS Assistant",
        menu
    )

    icon.run()
    TRAY_RUNNING = False


