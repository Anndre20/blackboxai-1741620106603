import React from 'react';
import AIAgentChat from './components/AIAgentChat';
import FileSorter from './components/FileSorter';

function App() {
    return (
        <div className="min-h-screen bg-gray-100">
            {/* Header */}
            <header className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
                    <h1 className="text-2xl font-bold text-gray-900">
                        Darion - Your AI-Powered Digital Assistant
                    </h1>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                <div className="bg-white rounded-lg shadow p-6">
                    <div className="mb-6">
                        <h2 className="text-lg font-medium text-gray-900">
                            Your Personal AI Assistant
                        </h2>
                        <p className="mt-1 text-sm text-gray-500">
                            Ask questions, manage emails, sync calendars, and more. I'm here to help!
                        </p>
                    </div>
                    
                    {/* AI Agent Chat Component */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <AIAgentChat />
                        <FileSorter />
                    </div>
                </div>

                {/* Features Section */}
                <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {/* Microsoft Integration */}
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                                    </svg>
                                </div>
                                <div className="ml-5">
                                    <h3 className="text-lg font-medium text-gray-900">Microsoft Integration</h3>
                                    <p className="mt-2 text-sm text-gray-500">
                                        Seamlessly sync with Outlook, OneDrive, and other Microsoft services
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Gmail Integration */}
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div className="ml-5">
                                    <h3 className="text-lg font-medium text-gray-900">Gmail Integration</h3>
                                    <p className="mt-2 text-sm text-gray-500">
                                        Manage your Gmail inbox and keep everything in sync
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* TimeTree Integration */}
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                        <div className="p-5">
                            <div className="flex items-center">
                                <div className="flex-shrink-0">
                                    <svg className="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div className="ml-5">
                                    <h3 className="text-lg font-medium text-gray-900">TimeTree Integration</h3>
                                    <p className="mt-2 text-sm text-gray-500">
                                        Keep your calendar organized with TimeTree synchronization
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-white mt-8">
                <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500">
                        © 2023 Darion. All rights reserved.
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
