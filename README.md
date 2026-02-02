# 🤖 JARVIS – Personal AI Desktop Assistant (Python)
A secure, voice-controlled, offline-first AI assistant inspired by Iron Man’s JARVIS, built fully in Python, optimized for low-end systems (Intel i3), with strong security, privacy, and automation features.
![image](https://wallpapercat.com/w/full/3/b/b/2141150-1920x1200-desktop-hd-jarvis-iron-man-wallpaper-photo.jpg)

🚀 Key Highlights
🎙️ Wake-word based voice assistant (Jarvis)
🔐 Voice authentication (owner only)
🔢 PIN-protected sensitive actions
🧠 AI responses only when required
🌐 Multilingual support (English + Hindi)
🖥️ System automation (Windows)
🧾 Encrypted logs & local data only
⚡ Optimized for low-end hardware (i3)

🧠 System Requirements
Component	Requirement
OS	Windows 10 / 11
CPU	Intel i3 (tested)
RAM	8 GB (works on 4 GB with limits)
Python	3.13+
Internet	Optional (AI features only)
Microphone	Required


🧩 Tech Stack
Python 3.13
Speech Recognition
Text-to-Speech (TTS)
OpenAI / AI Engine
Google Translator
PyAutoGUI
Psutil
Secure local storage (custom crypto)


📁 Project Structure (Simplified)
JARVIS/
│
├── main.py                  # Core brain
├── ai_engine.py             # AI logic
├── voice_input.py           # Speech recognition
├── voice_output.py          # TTS
├── voice_auth.py            # Voice authentication
├── pin_auth.py              # PIN security
├── secure_storage.py        # Encryption / Decryption
├── secure_actions.py        # Protected system actions
├── reminders_manager.py
├── language/
│   └── language_manager.py
├── vision/
│   └── screen_reader.py
├── code_runner/
│   └── runner.py
├── gui_dashboard.py
├── tray_manager.py
├── config.py
└── README.md****



🔐 Security & Privacy (Milestone 12 ✅)

✔ Voice authentication (only registered owner)
✔ PIN required for:
Delete files
Shutdown / Restart
Kill process
Read screen
Send email
Run Python / C++ files
✔ Encrypted command logs
✔ Local processing (no cloud storage)
✔ Mic disable / enable command
✔ Email credentials secured via config
✔ Security event logging



🗣️ Voice Commands (Examples)
🔑 Activation
Jarvis
⏰ Time & Date
What is time
Abhi ka samay
What is today's date

Multithreading

Tray + GUI Dashboard
