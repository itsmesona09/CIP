# 🎓 AURA - Attendance with Unique Recognition and Audio

AURA is an AI-powered smart classroom assistant that marks student attendance using face verification and voice recognition.

---

## 🚀 Features

- ✅ **Teacher Face Verification** using DeepFace
- 🎤 **Voice Recognition** to capture student names via microphone
- 📜 **Attendance Logging** stored as JSON with timestamps
- 💡 Runs in real-time with webcam & microphone integration
- ⛔ Graceful shutdown on exit (`Ctrl+C` or `q` key)

---

## 🖥️ Requirements

Install dependencies with:

```bash
pip install opencv-python deepface SpeechRecognition pyaudio
