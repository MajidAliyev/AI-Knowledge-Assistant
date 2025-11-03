import { useState, useEffect, useRef } from 'react'
import ChatInterface from './components/ChatInterface'
import Sidebar from './components/Sidebar'
import UploadModal from './components/UploadModal'
import { useTheme } from './hooks/useTheme'

function App() {
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false)
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const { theme, toggleTheme } = useTheme()

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'dark' : ''}`}>
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        <Sidebar 
          onUploadClick={() => setIsUploadModalOpen(true)}
          refreshTrigger={refreshTrigger}
          theme={theme}
          toggleTheme={toggleTheme}
        />
        <div className="flex-1 flex flex-col">
          <ChatInterface 
            onUploadClick={() => setIsUploadModalOpen(true)}
            refreshTrigger={refreshTrigger}
          />
        </div>
        <UploadModal
          isOpen={isUploadModalOpen}
          onClose={() => setIsUploadModalOpen(false)}
          onSuccess={() => {
            setRefreshTrigger(prev => prev + 1)
            setIsUploadModalOpen(false)
          }}
        />
      </div>
    </div>
  )
}

export default App

