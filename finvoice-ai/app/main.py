from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.intent_parser import parse_intent
from app.process_query import process_query
from pydantic import BaseModel
from fastapi import UploadFile, File
import shutil
from faster_whisper import WhisperModel

app = FastAPI()
print("Loading Whisper model...")

whisper_model = WhisperModel(
    "base",
    compute_type="int8"
)

print("Whisper Loaded")
class QueryRequest(BaseModel):
    query: str
    
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REQUEST MODEL
class QueryRequest(BaseModel):
    query: str

# HOME ROUTE
@app.get("/")
def home():

    return {
        "message": "Backend Running"
    }

# BALANCE ROUTE
@app.get("/balance/{name}")
def get_balance(name: str):

    return {
        "name": name,
        "balance": 247830
    }

# AI QUERY ROUTE
@app.post("/ask")
def ask_ai(data: QueryRequest):

    user_query = data.query

    print("\nUSER QUERY:", user_query)

    # STEP 1 → INTENT PARSING
    intent = parse_intent(user_query)

    print("\nINTENT:", intent)

    # STEP 2 → QUERY PROCESSING
    result = process_query(intent)

    print("\nRESULT:", result)

    return {
        "response": str(result)
    }

@app.post("/voice")
async def voice_ai(file: UploadFile = File(...)):

    # SAVE AUDIO
    audio_path = "temp_audio.webm"

    with open(audio_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    print("\nAudio Received")

    # TRANSCRIBE
    segments, info = whisper_model.transcribe(audio_path)

    transcript = ""

    for segment in segments:

        transcript += segment.text

    print("\nTRANSCRIPT:")
    print(transcript)

    # AI INTENT
    intent = parse_intent(transcript)

    print("\nINTENT:")
    print(intent)

    # DATABASE QUERY
    result = process_query(intent)

    print("\nRESULT:")
    print(result)

    return {
        "transcript": transcript,
        "response": str(result)
    }