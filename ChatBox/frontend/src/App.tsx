import React, { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import DocumentUpload from './components/DocumentUpload'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'documents'>('chat')

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Intelligent Chatbot
              </h1>
            </div>
            <nav className="flex space-x-8">
              <button
                onClick={() => setActiveTab('chat')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'chat'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Chat
              </button>
              <button
                onClick={() => setActiveTab('documents')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'documents'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Documents
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {activeTab === 'chat' ? (
          <ChatInterface />
        ) : (
          <DocumentUpload />
        )}
      </main>
    </div>
  )
}

export default App
