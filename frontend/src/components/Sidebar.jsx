import { useState, useEffect } from 'react'
import { Moon, Sun, Database, RefreshCw } from 'lucide-react'
import { statusAPI } from '../utils/api'

export default function Sidebar({ onUploadClick, refreshTrigger, theme, toggleTheme }) {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchStatus = async () => {
    try {
      setLoading(true)
      const data = await statusAPI.getStatus()
      setStatus(data)
    } catch (error) {
      console.error('Error fetching status:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStatus()
  }, [refreshTrigger])

  return (
    <div className="w-64 bg-gray-100 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Settings
        </h2>
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          title="Toggle theme"
        >
          {theme === 'dark' ? (
            <Sun className="w-5 h-5 text-gray-700 dark:text-gray-300" />
          ) : (
            <Moon className="w-5 h-5 text-gray-700 dark:text-gray-300" />
          )}
        </button>
      </div>

      {/* Status */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2 mb-3">
          <Database className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          <h3 className="text-sm font-medium text-gray-900 dark:text-white">
            Database Status
          </h3>
          <button
            onClick={fetchStatus}
            disabled={loading}
            className="ml-auto p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            title="Refresh status"
          >
            <RefreshCw className={`w-4 h-4 text-gray-500 dark:text-gray-400 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
        
        {loading ? (
          <div className="text-sm text-gray-500 dark:text-gray-400">Loading...</div>
        ) : status ? (
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Documents:</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {status.documents_indexed || 0}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Chunks:</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {status.chunks_stored || 0}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">Model:</span>
              <span className="font-medium text-gray-900 dark:text-white text-xs">
                {status.model || 'N/A'}
              </span>
            </div>
          </div>
        ) : (
          <div className="text-sm text-red-600 dark:text-red-400">
            Unable to fetch status
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
          Quick Actions
        </h3>
        <button
          onClick={onUploadClick}
          className="w-full px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-sm font-medium transition-colors"
        >
          Upload Documents
        </button>
      </div>

      {/* Footer */}
      <div className="mt-auto p-4 text-xs text-gray-500 dark:text-gray-400">
        <p>AI Knowledge Assistant</p>
        <p className="mt-1">v1.0.0</p>
      </div>
    </div>
  )
}

