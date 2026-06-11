# AddaAI - The AI-Powered Intellectual Roundtable

**AddaAI** is a premium, real-time generative AI debate platform designed to revive Bengal's legendary intellectual "Adda" culture. Users can enter any topic and witness a deeply contextual, historically accurate roundtable discussion between **Rabindranath Tagore**, **Satyajit Ray**, and **Subhas Chandra Bose**, moderated and summarized automatically.

---

## 🏛 System Architecture

AddaAI is built on a modern, highly optimized stack prioritizing real-time performance, clean architecture, and minimal AI inference latency.

### Tech Stack
- **Frontend**: Next.js 15, React 19, Tailwind CSS v4, Framer Motion, Zustand.
- **Backend**: Python 3.10+, FastAPI, WebSockets, SQLAlchemy, SQLite/PostgreSQL.
- **AI / LLM**: Groq API (Llama 3.3 70B Speculative Decoding) for ultra-fast generation.
- **RAG Pipeline**: ChromaDB (Vector Store), Sentence-Transformers (`all-MiniLM-L6-v2`), PyPDF / unstructured parsers.

### High-Level Components
1. **Interactive Client (Next.js)**: Handles real-time DOM updates, Framer Motion sequence animations, and connection persistence via Zustand stores.
2. **Websocket Engine (FastAPI)**: Manages concurrent bidirectional streaming to keep the UI perfectly synchronized with the multi-agent generation loop.
3. **RAG Service**: Dynamically fetches historical context specific to the active persona to ground the LLM's responses in factual, historical writing.
4. **Debate Orchestrator**: Enforces the rigid conversational sequence and intelligently trims historical context to preserve AI tokens.

---

## 🔄 Core Conversational Flow

The application enforces a strict, synchronous sequence to guarantee narrative continuity.

1. **Initialization**: The User inputs a topic string. A unique `DebateSession` is created in the database.
2. **WebSocket Handshake**: The client connects to `ws://localhost:8000/api/v1/debate/ws/{session_id}`.
3. **Debate Cycle**:
   - The orchestrator targets the first persona (**Tagore**).
   - The RAG system queries ChromaDB using the active topic to fetch relevant historical excerpts.
   - Groq generates a response using a compound prompt (System Prompt + RAG Context + Trimmed Chat History).
   - The response is persisted to the database and streamed to the UI.
   - The cycle repeats sequentially for **Ray** and **Bose**.
4. **Moderation**: Once the historical figures have spoken, the **Moderator** persona is invoked to summarize the diverse viewpoints.
5. **Follow-Up**: The User inputs a follow-up question. The backend saves the user message and restarts the Debate Cycle at step 3, using the user's latest question for the new RAG query.

---

## 🚀 Key Optimizations

- **Token Trimming**: The backend strictly limits conversational history to the last 6 messages (`context[-6:]`). This prevents exponential context-window growth, slashing Groq API costs and preventing out-of-memory errors.
- **Asynchronous RAG Retrieval**: ChromaDB lookups are handled via `asyncio.to_thread()`, ensuring the main FastAPI event loop is never blocked during disk/network I/O.
- **Resilient AI Fallbacks**: If the RAG vector store fails or is unpopulated, the system gracefully degrades to generic system prompts without interrupting the live WebSocket connection.
- **DOM & Mobile Optimization**: The frontend utilizes `100dvh` constraints and fully decoupled, absolute-positioned input containers to guarantee the UI never breaks during virtual keyboard invocations on mobile devices.

---

## 💻 Local Setup & Development

### 1. Clone & Environment
```bash
git clone https://github.com/your-org/adda-ai.git
cd adda-ai
```

### 2. Backend (FastAPI + Groq)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Create .env and add your Groq API Key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run database migrations / seed the DB
python check_db.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

Navigate to [http://localhost:3000](http://localhost:3000) to begin an Adda session.
