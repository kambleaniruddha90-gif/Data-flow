# Interview System: End-to-End Data Pipeline

📌 **Project Overview**

- This project establishes a robust Phase 1 System Foundation for an AI-based Interviewer. 
- It solves the critical problem of data consistency by ensuring that audio, video, and text processing modules communicate through defined JSON schemas, preventing pipeline breakage during simultaneous processing.

## 🎯 Objective

- **Prevent Broken Pipelines:** 
Strict data validation between modules.
- **Multimodal Integration:**
Simultaneous processing of audio (Mic), video (Camera), and text (LLM).
- **Reliability:**
Built-in failure flows for API timeouts and empty inputs.

### 📂  Project Structure


``` interview_system/
-├── app.py                  # Main 
-├── io_layer/               # Hardware Interface Layer
-│   ├── audio_stream.py     # Mic input & silence detection
-│   ├── camera_stream.py    # OpenCV webcam feed
-│   └── tts.py              # Text-to-Speech output (pyttsx3)
-├── modules/
-│   ├── stt_engine.py       # Whisper-based Speech-to-Text [cite: 1]
-│   ├── vision.py           # YOLO/OpenCV risk monitoring
-│   └── brain.py            # Evaluation & Decision Engine
-├── pipeline/
-│   └── orchestrator.py     # Logic for step-by-step data flow
-├── logs/                   # JSON storage for every turn
-├── requirements.txt        # System dependencies

```

## 🛠️Data Pipeline & Formats

**A. Speech-to-Text (STT)**

- Converts raw audio arrays into structured text data. 
  
```- Output Format:JSON{
  "status": "success",
  "text": "I have experience in Python.",
  "confidence": 0.9,
  "error": null
}
```

**B. Monitoring Pipeline (Vision)**

- Analyzes camera frames to detect objects and calculate a suspicious behavior score.
  
```- Output Format:JSON{
  "status": "success",
  "detections": [{"object": "person", "confidence": 0.95}],
  "risk_score": 0.1
}

```

**C. Evaluation & Decision (Brain)**

Processes the transcript to generate a score and determine the next interview step.

- **Decision Types:**
next_question: Moves to the next topic if score _> 7.

- **repeat:**
Asks for elaboration if the answer is too short.
flag_for_review: Triggered if risk_score > 0.7.

## ⚠️Failure Flow Mapping

The system is designed to handle edge cases without crashing:

- **STT Failure:**
The orchestrator.py includes a 3x Retry Logic. 
If all retries fail, it marks the answer as "No answer" to keep the pipeline moving.

- **Silence Detection:**
The audio_stream.py checks for mean amplitude; if the user is silent, the turn is skipped to save processing power.

- **Empty Input:**
If the LLM receives an empty string, the Brain defaults the score to 0 and triggers a "Repeat" prompt.

## 💾 Storage Points

**Data is persisted at the following stages:**
- **Turn Level:**
Every Q&A cycle is appended to self.history.
- **Session Level:**
On program exit, the entire history is saved to logs/[UUID].json.
- **Final Report:**
Includes total_questions, average_score, and a final_decision (Pass/Fail).

### 🚀 Installation & Setup
- **1. Install Requirements:**

```Bash
pip install -r requirements.txt

```
- **2.Run the System:**

```Bash
python app.py
```
## ✅ Acceptance Criteria Met

- **End-to-End Flow:**
Covers everything from Mic input to TTS output.
- **Defined I/O:** 
Every module utilizes the defined JSON structure.
- **Risk Engine:**
Monitoring runs concurrently with the interview flow.
- **Consistency:** 
UUID tracking ensures all logs are tied to a unique session.
