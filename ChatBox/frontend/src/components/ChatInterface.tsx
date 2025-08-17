import React, { useState, useRef, useEffect } from 'react'
import { Send, Bot, User } from 'lucide-react'
import { sendMessage, getChatHistory } from '../services/api'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

interface ChatResponse {
  answer: string
  conversation_id: number
  message_id: number
  sources: string[]
  tokens_used?: number
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [userId] = useState(1) // Mock user ID for demo
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Load chat history on component mount
    loadChatHistory()
  }, [])

  const loadChatHistory = async () => {
    try {
      const history = await getChatHistory(userId)
      if (history.conversations && history.conversations.length > 0) {
        const lastConversation = history.conversations[0]
        setMessages(lastConversation.messages || [])
      }
    } catch (error) {
      console.error('Failed to load chat history:', error)
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response: ChatResponse = await sendMessage({
        user_id: userId,
        message: inputMessage
      })

      const botMessage: Message = {
        id: response.message_id,
        role: 'assistant',
        content: response.answer,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage: Message = {
        id: Date.now(),
        role: 'assistant',
        content: 'Xin lỗi, đã xảy ra lỗi. Vui lòng thử lại.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border">
        {/* Chat Header */}
        <div className="px-6 py-4 border-b bg-gray-50 rounded-t-lg">
          <h2 className="text-lg font-medium text-gray-900">Chat với AI Assistant</h2>
          <p className="text-sm text-gray-500">
            Hỏi bất kỳ điều gì và nhận câu trả lời thông minh
          </p>
        </div>

        {/* Messages */}
        <div className="h-96 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Bot className="mx-auto h-12 w-12 text-gray-300 mb-4" />
              <p>Bắt đầu cuộc trò chuyện bằng cách gửi tin nhắn đầu tiên!</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`flex items-start space-x-3 max-w-xs lg:max-w-md ${
                    message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                  }`}
                >
                  <div
                    className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className="w-4 h-4" />
                    ) : (
                      <Bot className="w-4 h-4" />
                    )}
                  </div>
                  <div
                    className={`px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="text-sm">{message.content}</p>
                    <p
                      className={`text-xs mt-1 ${
                        message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                      }`}
                    >
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="px-4 py-2 rounded-lg bg-gray-100">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-6 py-4 border-t bg-gray-50 rounded-b-lg">
          <div className="flex space-x-4">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Nhập tin nhắn của bạn..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
