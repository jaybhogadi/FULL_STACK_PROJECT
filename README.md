# 🎓 AI-Powered Video Transcription and MCQ Generator

A full-stack MERN application to upload lecture videos (MP4), transcribe them using Whisper, segment the transcript into 5-minute chunks, and generate MCQs using a locally hosted LLM like Mistral (via Ollama). All processes run locally to ensure **offline capability** and **data privacy**.

## Demo

📥 [Sample Video File](https://drive.google.com/file/d/1-NBf8gVbPxj8QBQq1ALoxalMs_NP7Rdj/view?usp=sharing)

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
