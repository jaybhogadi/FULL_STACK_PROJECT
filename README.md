# 🎓 AI-Powered Video Transcription and MCQ Generator

A full-stack MERN application to upload lecture videos (MP4), transcribe them using Whisper, segment the transcript into 5-minute chunks, and generate MCQs using a locally hosted LLM like Mistral (via Ollama). All processes run locally to ensure **offline capability** and **data privacy**.

## 🔥 Live Demo

📥 [Sample Video File]([https://drive.google.com/your-demo-video-link](https://drive.google.com/file/d/1-NBf8gVbPxj8QBQq1ALoxalMs_NP7Rdj/view?usp=sharing))

---

## 🧩 Features

### ✅ Frontend (React.js + TypeScript + ShadCN + React Query)

- 📤 Upload MP4 video files (up to ~60 mins)
- ⚙️ Real-time progress status with WebSocket updates
- 📚 Segment-wise transcripts (5-minute intervals)
- ❓ MCQs generated per segment with explanations
- ✏️ Edit and 📥 Download MCQs or Transcripts

### ✅ Backend (Node.js + Express.js + TypeScript)

- 🧩 REST API endpoints for:
  - Uploading video
  - Transcribing content
  - Generating MCQs
- 🧠 Invokes Python backend (FastAPI) for AI tasks (Whisper + LLM)
- 🗂️ Stores video metadata, transcripts, and MCQs in MongoDB

### ✅ Python AI Backend (FastAPI + Ollama)

- 🎙️ [Whisper](https://github.com/openai/whisper) for transcription
- 💡 [Mistral](https://ollama.com/library/mistral) via Ollama for MCQ generation
- 🔌 Communicates with Node.js backend via REST APIs
- 💬 Prompts LLM to generate creative, relevant MCQs for each transcript segment

---

## 🛠️ Tech Stack

| Layer         | Tech                         |
| ------------- | ---------------------------- |
| Frontend      | React.js, TypeScript, ShadCN |
| Backend       | Node.js, Express.js, Routing-Controllers |
| Realtime Comm | WebSockets                   |
| AI Services   | Whisper, Mistral via Ollama  |
| Database      | MongoDB                      |
| Python AI API | FastAPI                      |

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/video-mcq-generator.git
cd video-mcq-generator
```

### 2. Environment Setup

#### `.env` for Node.js

```env
MONGO_USER=your_user
MONGO_PASSWORD=your_pass
MONGO_CLUSTER=cluster0.xxxxx.mongodb.net
MONGO_DB=vid_quiz
MONGO_URI=mongodb+srv://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_CLUSTER}/${MONGO_DB}?retryWrites=true&w=majority
```

> Make sure `.env` is in `.gitignore`.

#### `.env` for Python (Optional)

```env
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=mistral
```

---

### 3. Run Python Backend

> Assumes `ollama` and `whisper` are installed.

```bash
cd backend/python_fastapi
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### 4. Run Node.js Backend

```bash
cd backend
npm install
npm run dev
```

### 5. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📦 API Routes

### Node.js

| Endpoint               | Method | Description               |
| ----------------------|--------|---------------------------|
| `/upload`             | POST   | Uploads video             |
| `/transcribe`         | POST   | Sends video to Python API |
| `/generate-questions` | POST   | Triggers MCQ generation   |
| `/update-question`    | PUT    | Edit MCQ content          |

### Python (FastAPI)

| Endpoint           | Method | Description               |
|--------------------|--------|---------------------------|
| `/transcribe/`     | POST   | Transcribes audio (Whisper) |
| `/generate-mcqs/`  | POST   | Generates MCQs (LLM)      |

---

## 🧠 Sample Prompt (for LLM)

```text
Given the transcript below, generate 2 multiple-choice questions with 4 options each. Highlight the correct answer and give 1-line explanation.

Transcript:
"In this video, we're going to learn the anatomy and physiology of the ear..."
```

---

## 📋 To-Do / Future Enhancements

- [ ] Add user authentication (JWT)
- [ ] Enable export as PDF
- [ ] Add support for subtitles (SRT/VTT)
- [ ] Segment tuning via UI
- [ ] Dockerize full stack

---

## 👨‍💻 Author

**Jaya Krishna Sri Bhogadi**  
⚙️ Generative AI | MERN Developer | Whisper | Ollama | LangChain  
📧 jayakrishnasri13@gmail.com

---

## 🛡️ License

MIT License. See `LICENSE` file for details.
