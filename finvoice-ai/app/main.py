  # from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# from faster_whisper import WhisperModel

# import shutil

# from app.intent_parser import parse_intent
# from app.process_query import process_query

# # =========================
# # NEW IMPORT
# # Response formatter converts
# # raw database tuples into
# # human-friendly responses
# # =========================
# from app.response_formatter import format_response


# # =========================
# # FASTAPI APP
# # =========================

# app = FastAPI()


# # =========================
# # CORS
# # Allows frontend to connect
# # =========================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =========================
# # LOAD WHISPER MODEL
# # Speech-to-text model
# # =========================

# print("Loading Whisper model...")

# whisper_model = WhisperModel(
#     "base",
#     compute_type="int8"
# )

# print("Whisper model loaded successfully.")


# # =========================
# # REQUEST MODEL
# # Used for text API requests
# # =========================

# class QueryRequest(BaseModel):
#     query: str


# # =========================
# # HOME ROUTE
# # =========================

# @app.get("/")
# def home():

#     return {
#         "message": "FinVoice AI Backend Running"
#     }


# # =========================
# # MOCK BALANCE ROUTE
# # =========================

# @app.get("/balance/{name}")
# def get_balance(name: str):

#     return {
#         "name": name,
#         "balance": 247830
#     }


# # =========================
# # TEXT AI ROUTE
# # =========================

# @app.post("/ask")
# def ask_ai(data: QueryRequest):

#     try:

#         user_query = data.query

#         print("\nUSER QUERY:")
#         print(user_query)

#         # =========================
#         # STEP 1 → INTENT PARSING
#         # Converts user query into JSON intent
#         # =========================

#         intent_data = parse_intent(user_query)

#         print("\nINTENT1:")
#         print(intent_data)

#         # =========================
#         # STEP 2 → DATABASE PROCESSING
#         # Fetch raw database result
#         # =========================

#         result = process_query(intent_data)

#         print("\nRAW DATABASE RESULT:")
#         print(result)

#         # =========================
#         # STEP 3 → RESPONSE FORMATTING
#         # Converts ugly DB tuples into
#         # clean human-readable response
#         # =========================

#         formatted_response = format_response(
#             intent_data,
#             result
#         )

#         print("\nFORMATTED RESPONSE:")
#         print(formatted_response)

#         # =========================
#         # FINAL API RESPONSE
#         # =========================

#         return {
#             "success": True,
#             "query": user_query,
#             "intent": intent_data,
#             "response": formatted_response
#         }

#     except Exception as e:

#         print("\nERROR:")
#         print(str(e))

#         return {
#             "success": False,
#             "error": str(e)
#         }


# # =========================
# # VOICE AI ROUTE
# # =========================

# @app.post("/voice")
# async def voice_ai(file: UploadFile = File(...)):

#     try:

#         # =========================
#         # SAVE AUDIO FILE
#         # =========================

#         audio_path = "temp_audio.webm"

#         with open(audio_path, "wb") as buffer:

#             shutil.copyfileobj(file.file, buffer)

#         print("\nAudio received successfully.")

#         # =========================
#         # TRANSCRIBE AUDIO
#         # Speech → Text
#         # =========================

#         segments, info = whisper_model.transcribe(audio_path)

#         transcript = ""

#         for segment in segments:

#             transcript += segment.text + " "

#         transcript = transcript.strip()

#         print("\nTRANSCRIPT:")
#         print(transcript)

#         # =========================
#         # STEP 1 → INTENT PARSING
#         # =========================

#         intent_data = parse_intent(transcript)

#         print("\nINTENT:")
#         print(intent_data)

#         # =========================
#         # STEP 2 → DATABASE PROCESSING
#         # =========================

#         result = process_query(intent_data)

#         print("\nRAW DATABASE RESULT:")
#         print(result)

#         # =========================
#         # STEP 3 → RESPONSE FORMATTING
#         # =========================

#         formatted_response = format_response(
#             intent_data,
#             result
#         )

#         print("\nFORMATTED RESPONSE:")
#         print(formatted_response)

#         # =========================
#         # FINAL API RESPONSE
#         # =========================

#         return {
#             "success": True,
#             "transcript": transcript,
#             "intent": intent_data,
#             "response": formatted_response
#         }

#     except Exception as e:

#         print("\nVOICE ROUTE ERROR:")
#         print(str(e))

#         return {
#             "success": False,
#             "error": str(e)
#         }