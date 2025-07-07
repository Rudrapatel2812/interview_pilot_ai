# 🧠 AI Interview Practice Assistant

A dynamic, voice-driven mock interview system powered by Anthropic Claude and OpenAI APIs. Practice interviews using your own voice in a realistic, conversational loop with smart, persona-based interviewer agents.

---

## 📖 Description

Interviewing can be nerve-wracking — especially with unpredictable questions and high-pressure scenarios. This tool helps you build confidence through **realistic, personalized, voice-based mock interviews** tailored to your resume and job description.

You’ll speak naturally into your mic, and our AI will:

- 🎭 Role-play as an interviewer using Claude (Anthropic)
- 🧠 Listen to your responses using Whisper or live mic input
- 🗣️ Respond with intelligent follow-ups based on your background
- 🔊 Speak its replies aloud using OpenAI Text-to-Speech

Unlike scripted prep tools, this forces you to think on your feet in real time. Walk into your real interviews calm, confident, and conversational.

---

## 🚀 Features

- 🎤 Voice-to-text transcription via OpenAI Whisper
- 🤖 Interviewer logic powered by Claude 3 (Sonnet / Opus)
- 🗣️ Spoken responses using OpenAI TTS
- 🎭 Multiple interviewer personas (e.g., product manager, designer, quant)
- 📚 Context-aware questions and follow-ups based on your resume/job info
- 📝 Transcript logging for review and improvement

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/interview-pilot-ai.git
cd interview-pilot-ai-main
2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Add your API keys to .env
Inside the conversational-dialog/ folder, create a .env file:

OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

▶️ Usage

Option A — 🖥️ Command-line (Terminal)
python conversational-dialog/interviewer.py
This version uses your microphone input and plays audio responses using pygame.

Option B — 🌐 Web UI (Gradio)
python conversational-dialog/app.py
Then open your browser and go to:

http://localhost:7860
From here, speak directly into the mic and get dynamic audio + text responses.

🛠️ How We Built It

This project integrates:

OpenAI Whisper: Speech-to-text transcription
OpenAI TTS (Text-to-Speech): Spoken interviewer responses
Anthropic Claude: Interviewer dialogue generation
PyPDF2: Optional resume/job parsing
Pygame: Audio playback in CLI
Gradio: Browser-based interaction
The core logic dynamically creates interviewer personas and intelligent responses. You can extend it with custom roles, company contexts, or technical interview prep.

💬 Example Interviewer Personas

👔 Ethan — Strategic product manager at a climate tech startup
🎨 Nora — Visionary design lead at an ad agency
📈 Jordan — High-speed finance exec from Wall Street
🧮 Max — Logic-driven quant researcher at a hedge fund
Edit or add new personas inside the conversational-dialog/ directory as .txt prompt files.

🧾 Transcript

All conversation history is stored in:

interview_history.json
