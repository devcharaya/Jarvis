import os
import numpy as np
import librosa
import sounddevice as sd
import pickle

MODEL_FILE = "voice_model.pkl"
SAMPLE_RATE = 16000
DURATION = 3


def record_voice():
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    return audio.flatten()


def extract_features(audio):
    mfcc = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=20)
    return np.mean(mfcc.T, axis=0)


def enroll_owner():
    samples = []
    for i in range(5):
        print(f"Speak sample {i+1}/5")
        audio = record_voice()
        samples.append(extract_features(audio))

    model = np.mean(samples, axis=0)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    print("Voice enrolled successfully!")


def verify_speaker():
    if not os.path.exists(MODEL_FILE):
        return False

    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

    audio = record_voice()
    features = extract_features(audio)

    distance = np.linalg.norm(model - features)
    print("Voice distance:", distance)

    return distance < 50
