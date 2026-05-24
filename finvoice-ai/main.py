
from app.voice import record_audio, speech_to_text
from app.intent_parser import parse_intent
from app.process_query import process_query
from app.tts import speak
import json

while True:

    print("\nSpeak your banking query...")

    record_audio()

    text = speech_to_text()

    print("\nUser Said:")
    print(text)

    if "exit" in text.lower():
        speak("Goodbye")
        break

    intent_raw = parse_intent(text)

    intent_raw = intent_raw.replace("```json", "")
    intent_raw = intent_raw.replace("```", "")
    intent_raw = intent_raw.strip()

    print("\nIntent:")
    print(intent_raw)

    try:
        intent_json = json.loads(intent_raw)

    except:
        speak("Could not understand intent")
        continue

    result = process_query(intent_json)

    print("\nDatabase Result:")
    print(result)

    speak(result)