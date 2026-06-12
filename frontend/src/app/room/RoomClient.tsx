"use client"
import { useEffect, useState, useRef } from 'react';
import { useSearchParams } from 'next/navigation';
import { useDebateStore } from '@/store/useDebateStore';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Send, Clock } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const PERSONA_DETAILS: Record<string, { title: string, initials: string, color: string, bg: string, border: string }> = {
  'Rabindranath Tagore': { title: 'Poet • Philosopher', initials: 'RT', color: 'text-[#C9A227]', bg: 'bg-[#C9A227]/10', border: 'border-[#C9A227]/20' },
  'Satyajit Ray': { title: 'Filmmaker • Writer', initials: 'SR', color: 'text-[#B08968]', bg: 'bg-[#B08968]/10', border: 'border-[#B08968]/20' },
  'Subhas Chandra Bose': { title: 'Leader • Freedom Fighter', initials: 'SB', color: 'text-[#CBD5E1]', bg: 'bg-[#334155]/30', border: 'border-[#334155]' },
  'Moderator': { title: 'Discussion Summary', initials: 'MOD', color: 'text-[#94A3B8]', bg: 'bg-transparent', border: 'border-dashed border-[#334155]' },
  'You': { title: 'Participant', initials: 'U', color: 'text-[#F8FAFC]', bg: 'bg-[#1E293B]', border: 'border-[#334155]' }
};

export default function RoomClient() {
  const searchParams = useSearchParams();
  const id = searchParams.get('id') as string;
  const { messages, isTyping, activePersona, addMessage, setTyping } = useDebateStore();
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!id) return;
    
    // Clear previous messages when joining a new room
    useDebateStore.setState({ messages: [], activeSessionId: id });
    
    const wsBaseUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    const socket = new WebSocket(`${wsBaseUrl}/api/v1/debate/ws/${id}`);
    
    socket.onopen = () => {
      socket.send(JSON.stringify({ type: "start_debate" }));
    };
    
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      if (payload.type === "message") {
        addMessage({ ...payload.data, timestamp: new Date().toISOString() });
      } else if (payload.type === "status") {
        setTyping(payload.data.is_typing, payload.data.active_persona);
      }
    };

    setWs(socket);
    return () => socket.close();
  }, [id, addMessage, setTyping]);

  useEffect(() => {
    // Smooth auto-scroll
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages, isTyping]);

  const sendMsg = () => {
    if (!ws || !input.trim()) return;
    const msgContent = input;
    setInput('');
    ws.send(JSON.stringify({ type: "user_input", content: msgContent }));
  }

  const formatTime = (isoString?: string) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-[100dvh] bg-background relative overflow-hidden font-sans">
      {/* Decorative gradient */}
      <div className="absolute top-[-20%] right-[-10%] w-[50%] h-[50%] bg-[#C9A227]/5 rounded-full blur-[120px] pointer-events-none" />

      {/* Header */}
      <header className="px-6 py-4 border-b border-[#334155] bg-background/90 backdrop-blur-md z-20 shrink-0 flex items-center justify-between shadow-sm">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#F8FAFC]">AddaAI</h1>
          <p className="text-xs text-[#CBD5E1] mt-0.5 font-medium flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> Live Session
          </p>
        </div>
        <div className="flex -space-x-3">
          <Avatar className="border-2 border-background w-9 h-9 shadow-sm"><AvatarFallback className="text-xs bg-[#C9A227]/20 text-[#C9A227]">RT</AvatarFallback></Avatar>
          <Avatar className="border-2 border-background w-9 h-9 shadow-sm"><AvatarFallback className="text-xs bg-[#B08968]/20 text-[#B08968]">SR</AvatarFallback></Avatar>
          <Avatar className="border-2 border-background w-9 h-9 shadow-sm"><AvatarFallback className="text-xs bg-[#334155] text-[#CBD5E1]">SB</AvatarFallback></Avatar>
        </div>
      </header>
      
      {/* Main Chat Area */}
      <main ref={scrollContainerRef} className="flex-1 overflow-y-auto w-full z-10 pb-32 pt-6 px-4 md:px-8 scroll-smooth">
        <div className="max-w-3xl mx-auto space-y-8 flex flex-col">
          <AnimatePresence initial={false}>
            {messages.map((m, i) => {
              const details = PERSONA_DETAILS[m.persona] || PERSONA_DETAILS['Moderator'];
              const isUser = m.persona === 'You';
              const isMod = m.persona === 'Moderator';

              return (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, ease: "easeOut" }}
                  className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} w-full`}
                >
                  <div className={`flex items-end gap-3 max-w-[90%] md:max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                    
                    {/* Avatar */}
                    {!isMod && (
                      <Avatar className="w-10 h-10 shrink-0 border border-[#334155] shadow-sm mb-1">
                        <AvatarFallback className={`text-xs font-semibold ${details.bg} ${details.color}`}>
                          {details.initials}
                        </AvatarFallback>
                      </Avatar>
                    )}

                    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
                      {/* Meta Info */}
                      <div className={`flex items-center gap-2 mb-1.5 px-1 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                        <span className="text-sm font-semibold text-[#F8FAFC]">{m.persona}</span>
                        {!isUser && <span className="text-xs text-[#CBD5E1] hidden sm:inline-block">• {details.title}</span>}
                        {m.timestamp && (
                          <span className="text-[10px] text-muted-foreground flex items-center gap-1">
                            <Clock className="w-3 h-3" /> {formatTime(m.timestamp)}
                          </span>
                        )}
                      </div>

                      {/* Message Card */}
                      <Card className={`p-4 sm:p-5 rounded-2xl sm:rounded-3xl shadow-sm border ${details.border} ${isMod ? 'bg-transparent w-full' : 'bg-[#1E293B]'} ${isUser ? 'rounded-br-sm' : 'rounded-bl-sm'}`}>
                        {isMod && <div className="text-xs font-bold uppercase tracking-widest text-[#94A3B8] mb-3">Moderator Summary</div>}
                        <p className={`leading-relaxed text-[15px] sm:text-base whitespace-pre-wrap ${isMod ? 'text-[#CBD5E1] italic' : 'text-[#F8FAFC]'}`}>
                          {m.content}
                        </p>
                      </Card>
                    </div>

                  </div>
                </motion.div>
              )
            })}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && activePersona && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="flex items-end gap-3 max-w-[85%]"
            >
               <Avatar className="w-10 h-10 shrink-0 border border-[#334155] mb-1">
                  <AvatarFallback className="text-xs font-semibold bg-[#334155]/30 text-[#CBD5E1]">
                    {PERSONA_DETAILS[activePersona]?.initials || activePersona.charAt(0)}
                  </AvatarFallback>
                </Avatar>
              <div className="flex flex-col items-start">
                <span className="text-xs text-[#CBD5E1] mb-1.5 px-1 font-medium">{activePersona} is pondering...</span>
                <Card className="p-4 rounded-2xl rounded-bl-sm border border-[#334155] bg-[#1E293B]">
                  <div className="flex gap-1.5 items-center h-4 px-1">
                    <motion.span animate={{ y: [0, -4, 0] }} transition={{ repeat: Infinity, duration: 1, delay: 0 }} className="w-1.5 h-1.5 rounded-full bg-[#CBD5E1]" />
                    <motion.span animate={{ y: [0, -4, 0] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="w-1.5 h-1.5 rounded-full bg-[#CBD5E1]" />
                    <motion.span animate={{ y: [0, -4, 0] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-1.5 h-1.5 rounded-full bg-[#CBD5E1]" />
                  </div>
                </Card>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} className="h-4 w-full" />
        </div>
      </main>

      {/* Sticky Bottom Input Area */}
      <div className="absolute bottom-0 left-0 right-0 p-4 sm:p-6 bg-gradient-to-t from-background via-background/95 to-transparent z-30 pointer-events-none">
        <div className="max-w-3xl mx-auto pointer-events-auto">
          <div className="bg-[#1E293B] border border-[#334155] p-2 rounded-[2rem] shadow-xl flex items-center gap-2 backdrop-blur-xl ring-1 ring-black/5">
            <Input 
              value={input} 
              onChange={e => setInput(e.target.value)} 
              placeholder="Ask the Adda Panel a Question..." 
              onKeyDown={e => e.key === 'Enter' && sendMsg()} 
              className="flex-1 border-0 focus-visible:ring-0 bg-transparent px-4 sm:px-6 text-[#F8FAFC] placeholder:text-[#94A3B8] text-base h-12"
            />
            <Button 
              onClick={sendMsg} 
              disabled={!input.trim()} 
              size="icon" 
              className="rounded-full shrink-0 h-10 w-10 sm:h-12 sm:w-12 bg-[#C9A227] hover:bg-[#B08968] text-[#0F172A] transition-colors"
            >
              <Send className="h-4 w-4 sm:h-5 sm:w-5 ml-0.5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
