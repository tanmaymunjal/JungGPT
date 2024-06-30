"use client";
import { useState, useRef, useEffect } from 'react';
import Head from 'next/head';

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [npiScore, setNpiScore] = useState(33);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const fetchNpiScore = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/npi_score');
        const data = await response.json();
        setNpiScore(data.score);
      } catch (error) {
        console.error('Error fetching NPI score:', error);
      }
    };

    const interval = setInterval(fetchNpiScore, 3600000);

    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input }),
      });
      const data = await response.json();
      
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I couldn't process that request." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
      <div className="flex h-screen bg-gray-100">
        <div className="flex-grow flex flex-col overflow-hidden">
          <Head>
            <title>ChatGPT Clone</title>
            <link rel="icon" href="/favicon.ico" />
          </Head>
    
          <header className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
              <h1 className="text-2xl font-bold text-gray-900">JungGPT</h1>
            </div>
          </header>
    
          <main className="flex-grow overflow-hidden flex">
            <div className="flex-grow overflow-y-auto">
              <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                <div className="border-4 border-dashed border-gray-200 rounded-lg h-full flex flex-col">
                  <div className="flex-grow overflow-y-auto p-4 space-y-4">
                    {messages.map((message, index) => (
                      <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xl px-4 py-2 rounded-lg ${
                          message.role === 'user' 
                            ? 'bg-blue-500 text-white' 
                            : 'bg-green-500 text-white'
                        }`}>
                          <p className="font-semibold mb-1">{message.role === 'user' ? 'You' : 'Assistant'}</p>
                          {message.content}
                        </div>
                      </div>
                    ))}
                    <div ref={messagesEndRef} />
                  </div>
                  <form onSubmit={handleSubmit} className="p-4 bg-white">
                    <div className="flex rounded-md shadow-sm">
                      <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        className="flex-grow focus:ring-indigo-500 focus:border-indigo-500 block w-full rounded-none rounded-l-md sm:text-sm border-gray-300 text-black"
                        placeholder="Type your message..."
                        disabled={isLoading}
                      />
                      <button
                        type="submit"
                        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-r-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        disabled={isLoading}
                      >
                        {isLoading ? 'Sending...' : 'Send'}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
    
            <div className="w-64 bg-white shadow-lg p-4 flex-shrink-0 overflow-y-auto text-black">
              <h2 className="text-lg font-semibold mb-2">NPI 40 Score Bulletin</h2>
              <p className="text-3xl font-bold">{npiScore}</p>
              <p className="text-sm text-gray-500 mt-2">Updates every hour</p>
            </div>
          </main>
        </div>
      </div>
    );
}