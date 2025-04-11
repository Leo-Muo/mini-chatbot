"use client";

import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatInterface() {

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello! How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);


  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (input.trim() === "") return;
  
    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
  
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
  
      if (!response.ok) {
        console.log(response)
        const contentType = response.headers.get("content-type");
      
        if (contentType && contentType.includes("application/json")) {
          const errorData = await response.json();
          console.log(errorData.detail)
          throw new Error(errorData.detail || 'An error occurred');
        } else {
          const errorText = await response.text();
          console.log(errorText)
          throw new Error(errorText || `Error ${response.status}`);
        }

      }

      const data = await response.json();
  
      const aiMessage: Message = {
        role: "assistant", 
        content: data.message,
      };
  
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: `Sorry, there was an error: ${error instanceof Error ? error.message : "Unknown error"}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col mx-auto my-8 rounded-lg shadow max-w-4xl bg-gray-50">
  
      <div className="p-4 border-b bg-white rounded-t-lg">
        <h1 className="text-xl font-bold">Chat with Gunther</h1>
      </div>

      {/* Messages */}
      <div className="p-4 flex-1 overflow-auto space-y-4 h-96">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={message.role === "user" 
                ? "bg-blue-500 text-white rounded-2xl rounded-br-none p-3 max-w-xs" 
                : "bg-white border rounded-2xl rounded-bl-none p-3 max-w-xs"}
            >
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border rounded-2xl rounded-bl-none p-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-white rounded-b-lg">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-full"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="p-2 bg-blue-500 text-white rounded-full disabled:opacity-50"
            disabled={isLoading || input.trim() === ""}
          >
            <Send size={18} />
          </button>
        </form>
      </div>

      
    </div>
  );
}