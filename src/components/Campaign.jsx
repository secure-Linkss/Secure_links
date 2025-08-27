import { useState, useEffect } from 'react'

const Campaign = () => {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)
  const [expandedCampaign, setExpandedCampaign] = useState(null)
  const [analytics, setAnalytics] = useState({
    totalClicks: 0,
    realVisitors: 0,
    botsBlocked: 0,
    activeCampaigns: 0
  })

  useEffect(() => {
    fetchCampaigns()
    fetchAnalytics()
  }, [])

  const fetchCampaigns = async () => {
    try {
      const response = await fetch('/api/campaigns', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setCampaigns(data.campaigns || [])
      } else {
        console.error('Failed to fetch campaigns')
      }
    } catch (error) {
      console.error('Error fetching campaigns:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/analytics/overview', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setAnalytics({
          totalClicks: data.totalClicks || 0,
          realVisitors: data.realVisitors || 0,
          botsBlocked: data.totalClicks - data.realVisitors || 0,
          activeCampaigns: data.totalCampaigns || 0
        })
      }
    } catch (error) {
      console.error('Error fetching campaign analytics:', error)
    }
  }

  const toggleCampaignExpansion = (e, campaignId) => {
    e.stopPropagation();
    setExpandedCampaign(expandedCampaign === campaignId ? null : campaignId);
  };

  const handleCreateCampaign = async () => {
    const campaignName = prompt('Enter campaign name:')
    if (!campaignName || !campaignName.trim()) {
      return
    }
    
    try {
      const response = await fetch('/api/campaigns', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          name: campaignName.trim()
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        // Refresh campaigns list
        await fetchCampaigns()
        alert('Campaign created successfully!')
      } else {
        const errorData = await response.json()
        alert(errorData.error || 'Failed to create campaign')
      }
    } catch (error) {
      console.error('Error creating campaign:', error)
      alert('Failed to create campaign')
    }
  }

  const handleDeleteCampaign = async (campaignId) => {
    if (window.confirm('Are you sure you want to delete this campaign?')) {
      try {
        const response = await fetch(`/api/campaigns/${campaignId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        
        if (response.ok) {
          setCampaigns(campaigns.filter(c => c.id !== campaignId))
        }
      } catch (error) {
        console.error('Error deleting campaign:', error)
      }
    }
  }

  const handleToggleStatus = async (campaignId, currentStatus) => {
    try {
      const response = await fetch(`/api/campaigns/${campaignId}/toggle-status`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        setCampaigns(campaigns.map(c => 
          c.id === campaignId 
            ? { ...c, status: currentStatus === 'active' ? 'paused' : 'active' }
            : c
        ))
      }
    } catch (error) {
      console.error('Error toggling campaign status:', error)
    }
  }

  const handleCopyTrackingLink = (trackingId) => {
    const trackingUrl = `${window.location.origin}/t/${trackingId}?id={{id}}`
    navigator.clipboard.writeText(trackingUrl)
    alert('Tracking link copied to clipboard!')
  }

  if (loading) {
    return (
      <div className="p-6 space-y-6 bg-slate-900 min-h-screen">
        <div className="animate-pulse">
          <div className="h-8 bg-slate-700 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-24 bg-slate-700 rounded"></div>
            ))}
          </div>
          <div className="h-64 bg-slate-700 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6 bg-slate-900 min-h-screen">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 bg-purple-400 rounded-lg flex items-center justify-center">
            <span className="text-slate-900 font-bold">📊</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Campaign Management</h1>
            <p className="text-slate-400">Advanced campaign analytics and management dashboard</p>
          </div>
        </div>
        
        <div className="flex gap-2">
          <button 
            onClick={handleCreateCampaign}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg"
          >
            Create Campaign
          </button>
        </div>
      </div>

      {/* Compact Analytics Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <span className="text-blue-400 text-lg">👆</span>
            </div>
            <div>
              <p className="text-xs text-slate-400 uppercase tracking-wide">Total Clicks</p>
              <p className="text-xl font-bold text-white">{analytics.totalClicks.toLocaleString()}</p>
              <p className="text-xs text-green-400">Live Data</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-500/20 rounded-lg">
              <span className="text-green-400 text-lg">👥</span>
            </div>
            <div>
              <p className="text-xs text-slate-400 uppercase tracking-wide">Real Visitors</p>
              <p className="text-xl font-bold text-white">{analytics.realVisitors.toLocaleString()}</p>
              <p className="text-xs text-green-400">Live Data</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-500/20 rounded-lg">
              <span className="text-red-400 text-lg">🛡️</span>
            </div>
            <div>
              <p className="text-xs text-slate-400 uppercase tracking-wide">Bots Blocked</p>
              <p className="text-xl font-bold text-white">{analytics.botsBlocked.toLocaleString()}</p>
              <p className="text-xs text-green-400">Live Data</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-500/20 rounded-lg">
              <span className="text-purple-400 text-lg">📈</span>
            </div>
            <div>
              <p className="text-xs text-slate-400 uppercase tracking-wide">Active Campaigns</p>
              <p className="text-xl font-bold text-white">{analytics.activeCampaigns}</p>
              <p className="text-xs text-green-400">Live Data</p>
            </div>
          </div>
        </div>
      </div>

      {/* Campaign List */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg">
        <div className="p-4 border-b border-slate-700">
          <h3 className="text-lg font-bold text-white">Your Campaigns</h3>
          <p className="text-sm text-slate-400">Manage and monitor your tracking campaigns</p>
        </div>
        
        <div className="p-4">
          {campaigns.length === 0 ? (
            <div className="text-center py-12">
              <div className="mb-4">
                <span className="text-6xl">📊</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">No Campaigns Yet</h3>
              <p className="text-slate-400 mb-6">Create your first campaign to start tracking links and analyzing performance.</p>
              <button 
                onClick={handleCreateCampaign}
                className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium"
              >
                Create Your First Campaign
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {campaigns.map((campaign) => (
                <div key={campaign.id} className="bg-slate-700/50 rounded-lg border border-slate-600">
                  {/* Campaign Header */}
                  <div className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-3 h-3 rounded-full ${
                            campaign.status === 'active' ? 'bg-green-400' : 'bg-yellow-400'
                          }`}></div>
                          <div>
                            <h4 className="text-lg font-bold text-white">{campaign.name}</h4>
                            <p className="text-sm text-slate-400">ID: {campaign.trackingId}</p>
                          </div>
                        </div>
                        
                        <div className="flex gap-6 text-sm">
                          <div>
                            <p className="text-slate-400">Clicks</p>
                            <p className="font-bold text-white">{campaign.clicks.toLocaleString()}</p>
                          </div>
                          <div>
                            <p className="text-slate-400">Visitors</p>
                            <p className="font-bold text-white">{campaign.visitors.toLocaleString()}</p>
                          </div>
                          <div>
                            <p className="text-slate-400">Emails</p>
                            <p className="font-bold text-white">{campaign.emails.toLocaleString()}</p>
                          </div>
                          <div>
                            <p className="text-slate-400">Conv. Rate</p>
                            <p className="font-bold text-green-400">{campaign.conversionRate}%</p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleCopyTrackingLink(campaign.trackingId)}
                          className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm"
                          title="Copy tracking link"
                        >
                          📋 Copy
                        </button>
                        <button
                          onClick={() => handleToggleStatus(campaign.id, campaign.status)}
                          className={`px-3 py-1.5 rounded text-sm ${
                            campaign.status === 'active' 
                              ? 'bg-yellow-600 hover:bg-yellow-700 text-white' 
                              : 'bg-green-600 hover:bg-green-700 text-white'
                          }`}
                        >
                          {campaign.status === 'active' ? '⏸️ Pause' : '▶️ Resume'}
                        </button>
                        <button
                          onClick={(e) => toggleCampaignExpansion(e, campaign.id)}
                          className="px-3 py-1.5 bg-slate-600 hover:bg-slate-500 text-white rounded text-sm"
                        >
                          {expandedCampaign === campaign.id ? '🔼 Collapse' : '🔽 Expand'}
                        </button>
                        <button
                          onClick={() => handleDeleteCampaign(campaign.id)}
                          className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded text-sm"
                        >
                          🗑️ Delete
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  {/* Expanded Campaign Details */}
                  {expandedCampaign === campaign.id && (
                    <div className="border-t border-slate-600 p-4 bg-slate-800/50">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Campaign Info */}
                        <div>
                          <h5 className="font-semibold text-white mb-3">Campaign Details</h5>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span className="text-slate-400">Status:</span>
                              <span className={`font-medium ${
                                campaign.status === 'active' ? 'text-green-400' : 'text-yellow-400'
                              }`}>
                                {campaign.status === 'active' ? 'Active' : 'Paused'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Created:</span>
                              <span className="text-white">
                                {campaign.created ? new Date(campaign.created).toLocaleDateString() : 'N/A'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Tracking ID:</span>
                              <span className="text-white font-mono">{campaign.trackingId}</span>
                            </div>
                          </div>
                        </div>
                        
                        {/* Performance Metrics */}
                        <div>
                          <h5 className="font-semibold text-white mb-3">Performance</h5>
                          <div className="space-y-2 text-sm">
                            <div className="flex justify-between">
                              <span className="text-slate-400">Total Clicks:</span>
                              <span className="text-white font-bold">{campaign.clicks.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Unique Visitors:</span>
                              <span className="text-white font-bold">{campaign.visitors.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Email Captures:</span>
                              <span className="text-white font-bold">{campaign.emails.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-400">Conversion Rate:</span>
                              <span className="text-green-400 font-bold">{campaign.conversionRate}%</span>
                            </div>
                          </div>
                        </div>
                        
                        {/* Quick Actions */}
                        <div>
                          <h5 className="font-semibold text-white mb-3">Quick Actions</h5>
                          <div className="space-y-2">
                            <button 
                              onClick={() => handleCopyTrackingLink(campaign.trackingId)}
                              className="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm"
                            >
                              📋 Copy Tracking Link
                            </button>
                            <button className="w-full px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded text-sm">
                              📊 View Analytics
                            </button>
                            <button className="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded text-sm">
                              ⚙️ Edit Campaign
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Campaign

