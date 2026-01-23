"use client";

import { useChat } from '@ai-sdk/react';
import { useState } from 'react';
import { DefaultChatTransport } from 'ai';

export default function ChatApp() {
  // 1. You must manage your own input state now (AI SDK 5.0+ requirement)
  const [input, setInput] = useState('');

  // 2. Setup useChat with the new Transport architecture
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: 'http://localhost:8000/chat',
    }),
  });
  console.log("status:", status)
  console.log("message:", messages)
  // console.log("messages: " + JSON.stringify(messages, null, 2))
  // console.table(messages)
  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage({ text: input });
    setInput('');
  };

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
      <div className="space-y-4 mb-8">
        {messages.map((m) => (
          <div key={m.id} className="whitespace-pre-wrap">
            <p className="font-bold">{m.role === 'user' ? 'User: ' : 'AI: '}</p>
            {/* 4. Use m.parts (per your docs) to render content */}
            {m.parts.map((part, i) => {
              if (part.type === 'text') return <span key={i}>{part.text}</span>;
              return null;
            })}
          </div>
        ))}
        {status === 'streaming' && <div className="text-gray-400">AI is typing...</div>}
      </div>

      <form onSubmit={handleFormSubmit} className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl bg-white">
        <input
          className="w-full p-2 outline-none"
          value={input}
          placeholder="Say something..."
          onChange={(e) => setInput(e.target.value)}
        />
      </form>
    </div>
  );
}