import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

print("Model loaded.")

def record_audio():

    fs = 16000
    seconds = 8

    print("Speak now...")

    recording = sd.rec(
    int(seconds * fs),
    samplerate=16000,
    channels=1,
    dtype='int16'
)

    sd.wait()

    print(recording[:20])

    write("voice.wav", fs, recording.astype('int16'))

    print("Recording complete")

def speech_to_text():

    print("Transcribing audio...")

    segments, _ = model.transcribe("voice.wav")

    text = ""

    for segment in segments:
        text += segment.text

    return text