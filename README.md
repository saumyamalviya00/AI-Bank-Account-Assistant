# FinVoice AI

AI-powered voice banking assistant using:
- FastAPI
- Whisper
- Ollama
- PostgreSQL
- Next.js

## Features
- Voice-based banking queries
- AI intent detection
- Transaction analysis
- SQL query execution
- Whisper speech recognition
- Local LLM with Ollama

# FinVoice AI 🎙️🏦

AI-powered Voice Banking Assistant built using modern AI + Full Stack technologies.

FinVoice AI allows users to interact with banking information using natural voice commands. The system converts speech into text, understands user intent using Large Language Models, queries banking data from PostgreSQL, and returns conversational responses in real time.

---

# 🚀 What This Project Does

FinVoice AI simulates an intelligent banking voice assistant.

Users can:

* Speak banking queries using microphone
* Ask about account balance
* Check transaction history
* View sent/received money
* Get account details
* Interact with banking data conversationally

The project combines:

* Speech Recognition
* AI Intent Classification
* PostgreSQL Database Queries
* Conversational Response Formatting
* Frontend + Backend API Integration

---

# 🧠 How The System Works

```text
User Voice/Input
        ↓
Frontend (React + Vite)
        ↓
FastAPI Backend
        ↓
Whisper Speech Recognition
        ↓
Groq LLM Intent Parsing
        ↓
Query Builder / Database Engine
        ↓
PostgreSQL Database
        ↓
Response Formatter
        ↓
Frontend Response / Voice Output
```

---

# ✨ Features

## ✅ Voice Banking Assistant

Users can interact completely using voice.

Example:

* "What is my current balance?"
* "Show my last transaction"
* "Tell me about Rahul"

---

## ✅ AI Intent Detection

Groq LLM converts natural language into structured banking intents.

Example:

```json
{
  "intent": "show_balance"
}
```

---

## ✅ Speech-to-Text

Uses Faster Whisper for:

* microphone transcription
* real-time speech processing

---

## ✅ PostgreSQL Banking Database

Stores:

* users
* balances
* transaction history
* sender/receiver details

---

## ✅ Conversational Response Formatting

Converts raw database tuples into human-readable responses.

Example:

Instead of:

```python
[(10, 'Saumya', 'Rahul', Decimal('5000'))]
```

Returns:

```text
Your latest transaction was ₹5000 sent to Rahul.
```

---

# 🛠️ Tech Stack

| Technology | Purpose             |
| ---------- | ------------------- |
| Python     | Backend Development |
| FastAPI    | API Server          |
| PostgreSQL | Database            |
| React      | Frontend            |
| Vite       | Frontend Tooling    |
| Whisper    | Speech Recognition  |
| Groq       | AI Inference        |
| Llama 3.1  | Intent Parsing      |
| SQLAlchemy | Database ORM        |

---

# 📁 Project Structure

```text
finvoice-ai/
│
├── backend/
│   │
│   ├── app/
│   │   ├── intent_parser.py
│   │   ├── process_query.py
│   │   ├── response_formatter.py
│   │   ├── query_engine.py
│   │   ├── database.py
│   │   ├── voice.py
│   │   └── tts.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   │
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ Prerequisites

Before running this project, install:

## Required Software

* Python 3.10+
* Node.js 18+
* PostgreSQL
* Git

---

# 🔥 Complete Setup Guide

# 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/finvoice-ai.git
```

---

# 2️⃣ Navigate To Project

```bash
cd finvoice-ai
```

---

# 🗄️ PostgreSQL Database Setup

# 3️⃣ Open PostgreSQL

Create database:

```sql
CREATE DATABASE finvoice_ai;
```

---

# 4️⃣ Create Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    account_number VARCHAR(50),
    balance NUMERIC
);
```

---

# 5️⃣ Create Transactions Table

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(100),
    receiver VARCHAR(100),
    amount NUMERIC,
    transaction_type VARCHAR(50),
    transaction_date TIMESTAMP
);
```

---

# 6️⃣ Insert Sample Data

```sql
INSERT INTO users(name, account_number, balance)
VALUES
('Saumya','ACC1001',85000),
('Rahul','ACC1002',42000),
('Priya','ACC1003',92000);
```

---

```sql
INSERT INTO transactions(
    sender,
    receiver,
    amount,
    transaction_type,
    transaction_date
)
VALUES
('Saumya','Rahul',5000,'sent',NOW()),
('Rahul','Saumya',2000,'received',NOW());
```

---

# 🖥️ Backend Setup

# 7️⃣ Navigate To Backend

```bash
cd backend
```

---

# 8️⃣ Create Virtual Environment

## Windows

```bash
python -m venv venv
```

---

# 9️⃣ Activate Virtual Environment

## Windows

```bash
venv\Scripts\activate
```

---

# 🔟 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 1️⃣1️⃣ Create `.env` File

Inside backend folder:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# 1️⃣2️⃣ Run Backend Server

```bash
uvicorn main:app --reload
```

---

# 1️⃣3️⃣ Backend Running URLs

## API Base URL

```text
http://127.0.0.1:8000
```

---

## Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Frontend Setup

# 1️⃣4️⃣ Open New Terminal

Navigate to frontend:

```bash
cd frontend
```

---

# 1️⃣5️⃣ Install Frontend Dependencies

```bash
npm install
```

---

# 1️⃣6️⃣ Start Frontend

```bash
npm run dev
```

---

# 1️⃣7️⃣ Open Frontend

```text
http://localhost:5173
```

---

# 🎤 How Voice Processing Works

## Step-by-Step Voice Pipeline

### 1. User speaks through microphone

↓

### 2. Frontend records audio

↓

### 3. Audio sent to FastAPI backend

↓

### 4. Whisper converts speech → text

↓

### 5. Groq LLM detects banking intent

↓

### 6. Backend queries PostgreSQL database

↓

### 7. Response formatter creates conversational output

↓

### 8. Frontend displays response

---

# 🧪 Example Queries

## Balance Query

```text
What is my current bank balance?
```

---

## Transaction Query

```text
What was my last transaction?
```

---

## Account Details

```text
Tell me about Rahul
```

---

## Recent Payments

```text
Show my recent payments
```

---

## Money Sent

```text
How much money did I send to Rahul?
```

---

# 🔌 API Endpoints

| Method | Endpoint          | Description    |
| ------ | ----------------- | -------------- |
| GET    | `/`               | Backend status |
| POST   | `/ask`            | Text query     |
| POST   | `/voice`          | Voice query    |
| GET    | `/balance/{name}` | Balance API    |

---

# 🧠 AI Models Used

| Component          | Model                |
| ------------------ | -------------------- |
| Speech Recognition | Whisper Base         |
| Intent Parsing     | llama-3.1-8b-instant |
| AI Provider        | Groq                 |

---

# ⚠️ Common Errors & Fixes

# Backend Not Running

Error:

```text
ERR_CONNECTION_REFUSED
```

Fix:

```bash
uvicorn main:app --reload
```

---

# Groq API Error

Check:

```env
GROQ_API_KEY
```

---

# PostgreSQL Connection Error

Verify:

* PostgreSQL running
* correct DB URL
* tables created properly

---

# Microphone Not Working

Check:

* browser microphone permissions
* microphone selected correctly
* audio drivers installed

---

# 🚀 Future Improvements

* Speaker Verification
* JWT Authentication
* Real Banking APIs
* LangGraph Multi-Agent Workflow
* Voice Authentication
* Streaming Voice Responses
* Financial Analytics Dashboard
* AI Fraud Detection
* Transaction Categorization

---

# 📌 Current Status

✅ Frontend-Backend Connected
✅ Voice Query Processing
✅ AI Intent Parsing
✅ PostgreSQL Integration
✅ Conversational Responses
✅ Groq Integration
✅ Whisper Integration
✅ Real-Time API Communication

---

# 👨‍💻 Author

Saumya Malviya

---

# 📜 License

MIT License


# About requirements

Based on everything you built in your FinVoice AI project, these are the main requirements/dependencies you used across:

* backend
* AI
* speech recognition
* database
* frontend integration

---

# ✅ Complete Backend Requirements

## `requirements.txt`

```txt id="8jv4pd"
fastapi
uvicorn
pydantic
python-multipart

faster-whisper
sounddevice
scipy
numpy

groq
python-dotenv

sqlalchemy
psycopg2-binary

python-tts
torch
ctranslate2
```

---

# 🔍 WHY EACH PACKAGE IS USED

---

# 🌐 FastAPI Backend

| Package            | Purpose                     |
| ------------------ | --------------------------- |
| `fastapi`          | Backend API framework       |
| `uvicorn`          | FastAPI server              |
| `pydantic`         | Request/response validation |
| `python-multipart` | Upload voice/audio files    |

---

# 🎤 Speech Recognition

| Package          | Purpose                 |
| ---------------- | ----------------------- |
| `faster-whisper` | Speech-to-text          |
| `sounddevice`    | Record microphone audio |
| `scipy`          | Save/process audio      |
| `numpy`          | Audio array handling    |

---

# 🤖 AI / LLM

| Package         | Purpose              |
| --------------- | -------------------- |
| `groq`          | Groq API integration |
| `python-dotenv` | Load `.env` API keys |

---

# 🗄️ Database

| Package           | Purpose           |
| ----------------- | ----------------- |
| `sqlalchemy`      | Database ORM      |
| `psycopg2-binary` | PostgreSQL driver |

---

# 🧠 AI Framework (Optional)

You earlier used LangChain/Ollama.

| Package               | Purpose                |
| --------------------- | ---------------------- |
| `langchain`           | LLM orchestration      |
| `langchain-community` | Community integrations |

Now mostly optional since you moved to Groq directly.

---

# 🔊 Text To Speech

| Package      | Purpose      |
| ------------ | ------------ |
| `python-tts` | Voice output |

(Depends on your implementation.)

---

# ⚡ Whisper Internal Dependencies

These are used internally by Faster Whisper:

| Package       | Purpose              |
| ------------- | -------------------- |
| `torch`       | AI tensor operations |
| `ctranslate2` | Whisper optimization |

---

# ✅ Generate Exact Requirements Automatically

Inside backend:

```bash id="g6x2qp"
pip freeze > requirements.txt
```

This generates EXACT versions.

Example:

```txt id="m3v8tn"
fastapi==0.136.1
uvicorn==0.47.0
groq==0.31.0
sqlalchemy==2.0.43
```

---

# 🌐 FRONTEND REQUIREMENTS

Frontend uses:

* React
* Vite
* Axios

These are automatically stored in:

## `package.json`

---

# Main frontend dependencies probably are:

```json id="q7n4wc"
{
  "dependencies": {
    "react": "^19",
    "react-dom": "^19",
    "axios": "^1"
  }
}
```

---

# Dev dependencies:

```json id="t1m9zr"
{
  "devDependencies": {
    "vite": "^7"
  }
}
```

---

# 🔥 IMPORTANT

Your README should NOT manually list every internal package version unless needed.

Better approach:

# In README:

```markdown
## Install Backend Dependencies

pip install -r requirements.txt
```

---

# HOW TO CHECK WHAT YOU ACTUALLY USED

Run:

```bash id="x5k2jp"
pip list
```

OR:

```bash id="b8q4vn"
pip freeze
```

---

# YOUR CORE PROJECT STACK

This is the most important summary:

| Layer              | Technology       |
| ------------------ | ---------------- |
| Frontend           | React + Vite     |
| Backend            | FastAPI          |
| AI                 | Groq + Llama 3.1 |
| Speech Recognition | Faster Whisper   |
| Database           | PostgreSQL       |
| ORM                | SQLAlchemy       |
| Voice Recording    | sounddevice      |
| Deployment Server  | Uvicorn          |

---

# MOST IMPORTANT REQUIREMENTS FOR YOUR PROJECT

If someone clones your project, these are critical:

```txt id="y2m8pk"
fastapi
uvicorn
faster-whisper
groq
sqlalchemy
psycopg2-binary
python-dotenv
python-multipart
```

Without these:
project won't run.
