# 🤖 JARVIS – Personal AI Desktop Assistant (Python)
A secure, voice-controlled, offline-first AI assistant inspired by Iron Man’s JARVIS, built fully in Python, optimized for low-end systems (Intel i3), with strong security, privacy, and automation features.
![image](https://wallpapercat.com/w/full/3/b/b/2141150-1920x1200-desktop-hd-jarvis-iron-man-wallpaper-photo.jpg)

## Key Highlights

* **Wake-word based voice assistant** (Jarvis)
* **Voice authentication** (owner only)
* **PIN-protected sensitive actions**
* **AI responses only when required** (optimized performance)
* **Multilingual support** (English + Hindi)
* **System automation** (Windows)
* **Encrypted logs & local data only**
* **Optimized for low-end hardware** (Intel i3)

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Windows 10 / 11 |
| CPU | Intel i3 (tested) |
| RAM | 8 GB (works on 4 GB with limits) |
| Python | 3.13+ |
| Internet | Optional (AI features only) |
| Microphone | Required |

---

## Tech Stack

* **Python 3.13**
* **Speech Recognition**
* **Text-to-Speech (TTS)**
* **OpenAI / AI Engine**
* **Google Translator**
* **PyAutoGUI**
* **Psutil**
* **Secure local storage** (custom crypto)
* **Multithreading**
* **Tray + GUI Dashboard**

---

## Project Structure

```
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
└── README.md
```

---

## Security & Privacy (Milestone 12)

**Voice authentication** (only registered owner)

**PIN required for:**
* Delete files
* Shutdown / Restart
* Kill process
* Read screen
* Send email
* Run Python / C++ files

**Additional Security Features:**
* Encrypted command logs
* Local processing (no cloud storage)
* Mic disable / enable command
* Email credentials secured via config
* Security event logging

---

## Voice Commands

### Activation
```
Jarvis
```

### Time & Date
```
What is time
Abhi ka samay
What is today's date
```

### System Control
```
Open notepad
Open calculator
Lock PC
Take screenshot
Minimise all
```

### File Management
```
Create folder test
Open folder test
List files
Find file report.pdf
Delete file demo.txt   (PIN required)
```

### Reminders
```
Remind me to study at 9 PM
Set daily alarm at 7 AM
Snooze for 10 minutes
Stop alarm
```

### AI Knowledge (Only when needed)
```
What is Python
Black hole kya hota hai
Explain data science
```

**Note:** AI is NOT triggered for system commands.

### Multilingual Support
* Auto-detects language
* Hindi → English → AI → Voice output

### Screen Reading (Secure)
```
Read the screen   (PIN required)
```

### Developer Tools (Milestone 13)
```
Run python file test.py   (PIN required)
Compile C plus plus demo.cpp   (PIN required)
```

### Email (Secure)
```
Send email   (PIN required)
Yes
```

---

## AI Call Logic (Important Design)

**AI is called ONLY IF:**
* No system command matched
* Sentence length ≥ 2 words
* No system trigger word present
* Not a greeting or routine

**This avoids:**
* Overuse
* Delay on i3 CPU
* Wrong AI calls

---

## Testing Status

**Completed:**
* Wake word detection
* Voice authentication
* Hindi & English commands
* PIN lockout
* Email confirmation flow
* Screen reading
* AI fallback handling

Known issues are tracked and documented.

---

## Known Limitations

* AI may respond slowly on first call (i3)
* Screen reading output may be verbose
* No mobile app yet
* No face recognition yet
* No cloud sync (by design)

---

## Milestones Status

| Milestone | Status |
|-----------|--------|
| 1–5 Core Assistant | Done |
| 6–8 Automation | Done |
| 9–11 AI & Habits | Done |
| 12 Security & Privacy | Completed |
| 13 Advanced Features | Completed (Basic) |
| 14 Optimization & Stability | Pending |
| 15 UI, Animation & Release | Planned |

---

## Upcoming Features (Milestone 14 & 15)

* Performance optimization (i3 focused)
* AI caching
* Startup animation (real JARVIS feel)
* System health monitor
* Mobile controller (optional)
* Installer & portable build

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/jarvis-assistant.git
cd jarvis-assistant
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure settings:**
* Update `config.py` with your preferences
* Set up voice authentication
* Configure PIN security

**4. Run the assistant:**
```bash
python main.py
```

---

## Usage

**1. Activate Jarvis:**
* Say "Jarvis" to wake the assistant

**2. Voice Authentication:**
* Complete voice authentication on first run

**3. Give Commands:**
* Speak your command clearly
* Wait for response

**4. Secure Actions:**
* Enter PIN when prompted for sensitive operations

---

## Configuration

Edit `config.py` to customize:
* Wake word sensitivity
* Language preferences
* AI engine settings
* Security options
* Email credentials (encrypted)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Author

**Dev**  
MCA (Data Science)  
AI & System Automation Enthusiast  
India

---

## Acknowledgments

* OpenAI for AI capabilities
* Python community for excellent libraries
* All contributors and testers

---

## Final Note

**This project is not a toy assistant.**  
It is a **secure, privacy-focused, professional-grade AI desktop system**, built step-by-step with real engineering principles.

---

## Support

For issues, questions, or suggestions:
* Open an issue on GitHub
* Email: [your-email@example.com]
* Twitter: [@yourhandle]

---

## Disclaimer

This software is provided "as is" without warranty of any kind. Use at your own risk. The author is not responsible for any damages or security issues that may arise from the use of this software.
