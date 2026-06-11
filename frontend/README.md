# AddaAI Frontend Architecture & Flow

AddaAI is a real-time, generative AI discussion platform where users engage in intellectual debate with historical figures (Rabindranath Tagore, Satyajit Ray, and Subhas Chandra Bose). 

This repository contains the **Next.js 15 Frontend Client**, built for optimal reading experience, responsive design, and ultra-low latency WebSocket streaming.

---

## 🏛 UI Architecture

### Technology Stack
- **Framework**: Next.js 15 (React 19)
- **Styling**: Tailwind CSS v4, customized with a premium dark-mode aesthetic.
- **State Management**: Zustand (`useDebateStore.ts`) for managing WebSocket events and chat history globally.
- **Animations**: Framer Motion for subtle, non-blocking conversational entry and typing indicators.
- **Components**: Shadcn/Radix UI base components, heavily modified for a "museum-quality" reading experience.

### Core Architecture Principles
1. **Decoupled Connectivity**: The WebSocket connection operates strictly within `useEffect` hooks decoupled from the render cycle, relying on Zustand to pipe state globally without causing massive DOM re-renders.
2. **Resilient Layouts**: Using `100dvh` combined with independent `flex-1 overflow-y-auto` constraints, the layout is mathematically guaranteed to fit mobile viewports, immune to virtual keyboard shifts.
3. **Optimized Auto-Scroll**: Uses native DOM `scrollIntoView` attached to a safely anchored boundary `div`, executing smoothly via `requestAnimationFrame` and React hooks.

---

## 🔄 Conversational UX Flow

1. **Topic Submission**: User creates a debate via the `/topic-submission` route.
2. **Room Entry (`/room/[id]`)**: The UI mounts and opens a real-time WebSocket connection to the FastAPI backend.
3. **Sequential Stepping**:
   - The UI receives `"status"` events from the backend (e.g., `{"active_persona": "Rabindranath Tagore", "is_typing": true}`).
   - Framer Motion mounts the animated bouncing-dots typing indicator.
   - The UI receives the generated `"message"` payload. The message is pushed to the Zustand store, the typing indicator is destroyed, and the card elegantly fades in.
4. **Moderator & Follow-up**: After the AI panel responds, the Moderator summarizes the round. The **always-visible, sticky input bar** at the bottom allows the user to follow up.
5. **Continuous Loop**: The user's input is sent via WebSockets, instantly appending to the UI timeline, and restarting the debate sequence.

---

## 🎨 Design System

The platform strictly avoids generic neons and flashiness. The UI is governed by a curated, historically-inspired dark palette:
- **Background**: Deep Slate (`#0F172A`)
- **Card Background**: Muted Steel (`#1E293B`)
- **Tagore Accent**: Gold/Primary (`#C9A227`)
- **Ray Accent**: Sepia/Muted (`#B08968`)
- **Bose Accent**: Cool Slate (`#94A3B8`)

---

## 💻 Local Setup Instructions

First, ensure the FastAPI backend is running locally on port `8000`.

Then, install dependencies and start the Next.js development server:

```bash
# Install dependencies
npm install

# Start the dev server with Turbopack
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser. The Adda Room can be accessed directly or by starting a new topic from the homepage.
