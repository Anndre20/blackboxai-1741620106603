import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faSync, faTimes } from '@fortawesome/free-solid-svg-icons';

const AIAgentChat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const formatTimestamp = () => {
        return new Date().toLocaleTimeString();
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = {
            type: 'user',
            content: input,
            timestamp: formatTimestamp()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch('/api/ai-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: input }),
            });

            if (!response.ok) {
                throw new Error('Failed to get response from AI');
            }

            const data = await response.json();
            
            setMessages(prev => [...prev, {
                type: 'ai',
                content: data.response,
                timestamp: formatTimestamp()
            }]);
        } catch (err) {
            setError('Failed to get response. Please try again.');
            console.error('Error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = async () => {
        try {
            await fetch('/api/conversation/reset', {
                method: 'POST',
            });
            setMessages([]);
            setError(null);
        } catch (err) {
            setError('Failed to reset conversation');
            console.error('Error:', err);
        }
    };

    const handleSyncAll = async () => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch('/api/sync/all');
            if (!response.ok) {
                throw new Error('Failed to sync services');
            }

            const data = await response.json();
            
            setMessages(prev => [...prev, {
                type: 'ai',
                content: data.response,
                timestamp: formatTimestamp()
            }]);
        } catch (err) {
            setError('Failed to sync services. Please try again.');
            console.error('Error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[600px] max-w-4xl mx-auto bg-white rounded-lg shadow-lg">
            {/* Header */}
            <div className="flex justify-between items-center px-6 py-4 bg-blue-600 text-white rounded-t-lg">
                <h2 className="text-xl font-semibold">AI Assistant</h2>
                <div className="flex gap-2">
                    <button
                        onClick={handleSyncAll}
                        className="p-2 hover:bg-blue-700 rounded-full transition-colors"
                        title="Sync All Services"
                    >
                        <FontAwesomeIcon icon={faSync} className={isLoading ? 'animate-spin' : ''} />
                    </button>
                    <button
                        onClick={handleReset}
                        className="p-2 hover:bg-blue-700 rounded-full transition-colors"
                        title="Reset Conversation"
                    >
                        <FontAwesomeIcon icon={faTimes} />
                    </button>
                </div>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[70%] rounded-lg p-3 ${
                                message.type === 'user'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-800'
                            }`}
                        >
                            <div className="text-sm whitespace-pre-wrap">{message.content}</div>
                            <div className={`text-xs mt-1 ${
                                message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                            }`}>
                                {message.timestamp}
                            </div>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Error Message */}
            {error && (
                <div className="px-4 py-2 bg-red-100 text-red-600 text-sm">
                    {error}
                </div>
            )}

            {/* Input Form */}
            <form onSubmit={handleSubmit} className="p-4 border-t">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className={`px-4 py-2 bg-blue-600 text-white rounded-lg transition-colors
                            ${(isLoading || !input.trim()) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'}`}
                    >
                        <FontAwesomeIcon icon={faPaperPlane} />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AIAgentChat;
