import speech_recognition as sr
import wave

# Create a dummy 1-second blank WAV file
with wave.open("dummy.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(b'\x00' * 44100 * 2)

recognizer = sr.Recognizer()
try:
    with sr.AudioFile("dummy.wav") as source:
        audio = recognizer.record(source)
    print("Audio loaded properly. Now transcribing...")
    text = recognizer.recognize_whisper(audio, model="base")
    print("Transcription:", text)
except Exception as e:
    import traceback
    traceback.print_exc()
