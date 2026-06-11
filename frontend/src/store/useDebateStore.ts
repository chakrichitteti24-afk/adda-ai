import { create } from 'zustand';

export interface Message {
  id?: string;
  persona: string;
  content: string;
  timestamp?: string;
}

interface DebateState {
  activeSessionId: string | null;
  messages: Message[];
  isTyping: boolean;
  activePersona: string | null;
  setActiveSession: (id: string) => void;
  addMessage: (message: Message) => void;
  setTyping: (status: boolean, persona?: string | null) => void;
}

export const useDebateStore = create<DebateState>((set) => ({
  activeSessionId: null,
  messages: [],
  isTyping: false,
  activePersona: null,
  setActiveSession: (id) => set({ activeSessionId: id }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setTyping: (status, persona = null) => set({ isTyping: status, activePersona: persona }),
}));
