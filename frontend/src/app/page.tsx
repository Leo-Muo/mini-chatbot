import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <div className="items-center min-h-screen font-sans">
      <header className="flex flex-col items-center justify-center py-2 mt-8">
        <h1 className="text-4xl font-bold">AI Chatbot</h1>
      </header>
      <main className="items-center sm:items-start">
        <ChatInterface />
      </main>
    </div>
  );
}