import { useState, useRef, useEffect } from 'react'
import { Send, Upload, Loader2, AlertCircle, Wifi, WifiOff } from 'lucide-react'
import { chatAPI, statusAPI } from '../utils/api'
import MessageList from './MessageList'
import SourceCitations from './SourceCitations'

export default function ChatInterface({ onUploadClick, refreshTrigger }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentSources, setCurrentSources] = useState([])
  const [error, setError] = useState(null)
  const [isConnected, setIsConnected] = useState(true)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  // Check connection status
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await statusAPI.getStatus()
        setIsConnected(true)
        setError(null)
      } catch (err) {
        setIsConnected(false)
        setError('Cannot connect to backend server. Please ensure it is running on http://localhost:8000')
      }
    }
    
    checkConnection()
    const interval = setInterval(checkConnection, 10000) // Check every 10 seconds
    return () => clearInterval(interval)
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
      sources: [],
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setCurrentSources([])
    setError(null)

    try {
      const conversationHistory = messages.map(msg => ({
        role: msg.role,
        content: msg.content,
      }))

      const response = await chatAPI.sendMessage(input.trim(), conversationHistory)
      
      const assistantMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        sources: response.sources || [],
      }

      setMessages(prev => [...prev, assistantMessage])
      setCurrentSources(response.sources || [])
      setIsConnected(true)
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMsg = error.message || 'Sorry, I encountered an error processing your request. Please try again.'
      setError(errorMsg)
      setIsConnected(error.message?.includes('Cannot connect') ? false : true)
      
      const errorMessage = {
        role: 'assistant',
        content: errorMsg,
        timestamp: new Date(),
        sources: [],
        error: true,
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-800">
      {/* Header */}
      <div className="border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              AI Knowledge Assistant
            </h1>
            {isConnected ? (
              <Wifi className="w-5 h-5 text-green-500" title="Connected" />
            ) : (
              <WifiOff className="w-5 h-5 text-red-500" title="Disconnected" />
            )}
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Ask questions about your documents
          </p>
        </div>
        <button
          onClick={onUploadClick}
          className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors shadow-sm"
        >
          <Upload className="w-4 h-4" />
          Upload Documents
        </button>
      </div>
      
      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800 px-6 py-3 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
          <p className="text-sm text-red-800 dark:text-red-200 flex-1">{error}</p>
          <button
            onClick={() => setError(null)}
            className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-200"
          >
            ×
          </button>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 scrollbar-hide">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center max-w-2xl px-4">
              <div className="mb-6">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center">
                  <svg className="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
              </div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
                Welcome to your Knowledge Assistant
              </h2>
              <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
                Ask questions about your documents and get intelligent, cited answers powered by AI.
              </p>
              
              {!isConnected && (
                <div className="mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                  <p className="text-sm text-yellow-800 dark:text-yellow-200">
                    ⚠️ Backend not connected. Please start the backend server first.
                  </p>
                </div>
              )}
              
              <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 text-left">
                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                  💡 Try asking:
                </p>
                <ul className="space-y-3 text-sm text-gray-600 dark:text-gray-400">
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 dark:text-primary-400">•</span>
                    <span>"What were the key takeaways from that system-design book I read last month?"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 dark:text-primary-400">•</span>
                    <span>"Summarize my recent emails about project X"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 dark:text-primary-400">•</span>
                    <span>"What notes do I have about machine learning?"</span>
                  </li>
                </ul>
              </div>
              
              <div className="mt-8">
                <button
                  onClick={onUploadClick}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors shadow-lg hover:shadow-xl"
                >
                  <Upload className="w-5 h-5" />
                  Upload Your First Document
                </button>
              </div>
            </div>
          </div>
        ) : (
          <MessageList messages={messages} />
        )}
        {isLoading && (
          <div className="flex items-center gap-3 text-gray-500 dark:text-gray-400 py-4 px-2">
            <Loader2 className="w-5 h-5 animate-spin text-primary-600 dark:text-primary-400" />
            <span className="text-sm font-medium">Thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Sources */}
      {currentSources.length > 0 && (
        <div className="border-t border-gray-200 dark:border-gray-700 px-6 py-3">
          <SourceCitations sources={currentSources} />
        </div>
      )}

      {/* Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 px-6 py-4">
        <form onSubmit={handleSend} className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center gap-2"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                <Send className="w-5 h-5" />
                Send
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  )
}

