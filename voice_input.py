import speech_recognition as sr


def listen_voice():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)

        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text

    except sr.WaitTimeoutError:
        print("Listening timed out")
        return None

    except sr.UnknownValueError:
        print("Could not understand audio")
        return None

    except Exception:
        print("No input detected")
        return None
