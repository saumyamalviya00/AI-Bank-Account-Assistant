print("Starting test...")

from app.voice import record_audio, speech_to_text

import wave
import simpleaudio as sa

print("Recording will start now...")

# Record
record_audio()

print("Playing audio...")

# Play recorded audio
wave_read = wave.open("voice.wav", "rb")

audio_data = wave_read.readframes(wave_read.getnframes())

play_obj = sa.play_buffer(
    audio_data,
    wave_read.getnchannels(),
    wave_read.getsampwidth(),
    wave_read.getframerate()
)

play_obj.wait_done()

print("Converting speech to text...")

# Speech to text
text = speech_to_text()

print("\nRecognized Text:")
print(text)