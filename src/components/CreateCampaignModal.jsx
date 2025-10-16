import { useState } from 'react'
import { Plus } from 'lucide-react'

const CreateCampaignModal = ({ isOpen, onClose, onCampaignCreated }) => {
  const [campaignName, setCampaignName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!campaignName.trim()) {
      setError('Campaign name cannot be empty.')
      return
    }

    setLoading(true)
    setError('')

    try {
      // The backend logic for creating a campaign seems to be creating a link with a default URL
      // I will follow this pattern to ensure compatibility.
      const response = await fetch('/api/links', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        credentials: 'include',
        body: JSON.stringify({
          original_url: 'https://example.com', // Placeholder URL for campaign creation
          campaign_name: campaignName.trim(),
          title: campaignName.trim()
        })
      })

      if (response.ok) {
        const data = await response.json()
        onCampaignCreated(data.link)
        onClose()
        setCampaignName('')
      } else {
        const errorData = await response.json()
        setError(errorData.error || 'Failed to create campaign')
      }
    } catch (error) {
      setError('Network error occurred')
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-lg w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white">Create New Campaign</h3>
            <button 
              onClick={onClose}
              className="text-slate-400 hover:text-white"
            >
              ✕
            </button>
          </div>

          {error && (
            <div className="p-3 bg-red-900 text-red-300 border border-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Campaign Name *
              </label>
              <input
                type="text"
                placeholder="Enter a descriptive name for your campaign"
                value={campaignName}
                onChange={(e) => setCampaignName(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 text-white rounded-lg focus:border-blue-500 focus:outline-none"
                required
              />
            </div>
            
            <div className="flex gap-3 pt-4">
              <button 
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg"
              >
                Cancel
              </button>
              <button 
                type="submit"
                disabled={loading}
                className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 flex items-center justify-center"
              >
                {loading ? (
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <>
                    <Plus className="h-4 w-4 mr-2" />
                    Create Campaign
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default CreateCampaignModal
