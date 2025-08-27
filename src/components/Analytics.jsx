import { useState, useEffect } from 'react'

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d')
  const [loading, setLoading] = useState(true)
  const [analytics, setAnalytics] = useState({
    totalClicks: 0,
    uniqueVisitors: 0,
    conversionRate: 0,
    bounceRate: 0,
    capturedEmails: 0,
    activeLinks: 0
  })
  const [topCampaigns, setTopCampaigns] = useState([])
  const [devices, setDevices] = useState([])
  const [countries, setCountries] = useState([])

  useEffect(() => {
    fetchAnalyticsData()
  }, [timeRange])

  const fetchAnalyticsData = async () => {
    setLoading(true)
    try {
      // Fetch overview analytics
      const overviewResponse = await fetch('/api/analytics/overview', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (overviewResponse.ok) {
        const overviewData = await overviewResponse.json()
        setAnalytics({
          totalClicks: overviewData.totalClicks || 0,
          uniqueVisitors: overviewData.realVisitors || 0,
          conversionRate: overviewData.conversionRate || 0,
          bounceRate: 34.2, // This would need to be calculated from actual data
          capturedEmails: overviewData.capturedEmails || 0,
          activeLinks: overviewData.activeLinks || 0
        })
      }

      // Fetch campaigns data
      const campaignsResponse = await fetch('/api/campaigns', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (campaignsResponse.ok) {
        const campaignsData = await campaignsResponse.json()
        const campaigns = (campaignsData.campaigns || []).slice(0, 3).map(campaign => ({
          name: campaign.name,
          clicks: campaign.total_clicks || 0,
          conversions: Math.floor((campaign.total_clicks || 0) * (campaign.conversion_rate || 0) / 100),
          rate: campaign.conversion_rate || 0
        }))
        setTopCampaigns(campaigns)
      }

      // Fetch device analytics
      const devicesResponse = await fetch('/api/analytics/devices', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (devicesResponse.ok) {
        const devicesData = await devicesResponse.json()
        setDevices(devicesData || [])
      }

      // Fetch countries analytics
      const countriesResponse = await fetch('/api/analytics/countries', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (countriesResponse.ok) {
        const countriesData = await countriesResponse.json()
        setCountries((countriesData || []).slice(0, 4))
      }

    } catch (error) {
      console.error('Error fetching analytics data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    fetchAnalyticsData()
  }

  const handleExport = () => {
    // Implement export functionality
    console.log('Export analytics data')
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
          <div className="h-64 bg-slate-700 rounded mb-6"></div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="h-64 bg-slate-700 rounded"></div>
            <div className="h-64 bg-slate-700 rounded"></div>
          </div>
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
            <h1 className="text-2xl font-bold text-white">Analytics Dashboard</h1>
            <p className="text-slate-400">Your comprehensive performance overview</p>
          </div>
        </div>
        
        <div className="flex gap-2">
          <select 
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="bg-slate-800 border border-slate-600 text-white rounded-lg px-4 py-2"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
          <button 
            onClick={handleRefresh}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
          >
            🔄 Refresh
          </button>
          <button 
            onClick={handleExport}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
          >
            📥 Export
          </button>
        </div>
      </div>

      {/* Key Metrics - Compact Design */}
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
              <p className="text-xs text-slate-400 uppercase tracking-wide">Visitors</p>
              <p className="text-xl font-bold text-white">{analytics.uniqueVisitors.toLocaleString()}</p>
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
              <p className="text-xs text-slate-400 uppercase tracking-wide">Conv. Rate</p>
              <p className="text-xl font-bold text-white">{analytics.conversionRate}%</p>
              <p className="text-xs text-green-400">Live Data</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-500/20 rounded-lg">
              <span className="text-orange-400 text-lg">📧</span>
            </div>
            <div>
              <p className="text-xs text-slate-400 uppercase tracking-wide">Emails</p>
              <p className="text-xl font-bold text-white">{analytics.capturedEmails.toLocaleString()}</p>
              <p className="text-xs text-green-400">Live Data</p>
            </div>
          </div>
        </div>
      </div>

      {/* Traffic Trends Chart */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-white">Traffic Trends</h3>
            <p className="text-slate-400">Clicks, visitors, and conversions over time</p>
          </div>
          <div className="flex gap-2">
            <button className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm">
              📊 Clicks
            </button>
            <button className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm">
              👥 Visitors
            </button>
            <button className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm">
              📈 Conversions
            </button>
          </div>
        </div>
        
        {/* Chart Visualization */}
        <div className="bg-slate-900 rounded-lg p-6 h-64 relative">
          <div className="absolute inset-0 bg-gradient-to-t from-blue-900/20 to-transparent rounded-lg"></div>
          <div className="relative h-full flex items-end justify-between">
            {Array.from({ length: 7 }, (_, i) => {
              const height = Math.max(20, (analytics.totalClicks / 7) * (0.5 + Math.random() * 0.5))
              return (
                <div key={i} className="flex flex-col items-center gap-2">
                  <div 
                    className="bg-gradient-to-t from-blue-500 to-blue-400 rounded-t"
                    style={{ 
                      height: `${Math.min(height, 80)}%`, 
                      width: '20px' 
                    }}
                  ></div>
                  <span className="text-xs text-slate-400">
                    {new Date(Date.now() - (6-i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { weekday: 'short' })}
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Performance Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Campaigns */}
        <div className="bg-slate-800 border border-slate-700 rounded-lg">
          <div className="p-4 border-b border-slate-700">
            <h3 className="text-lg font-bold text-white">Top Performing Campaigns</h3>
            <p className="text-sm text-slate-400">Best campaigns by conversion rate</p>
          </div>
          <div className="p-4">
            {topCampaigns.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-slate-400">No campaign data available</p>
                <p className="text-slate-500 text-sm">Create campaigns to see performance data</p>
              </div>
            ) : (
              <div className="space-y-3">
                {topCampaigns.map((campaign, index) => (
                  <div key={campaign.name} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                        index === 0 ? 'bg-yellow-500/20' : index === 1 ? 'bg-blue-500/20' : 'bg-purple-500/20'
                      }`}>
                        <span className="text-lg">
                          {index === 0 ? '🏆' : index === 1 ? '🥈' : '🥉'}
                        </span>
                      </div>
                      <div>
                        <p className="font-medium text-white">{campaign.name}</p>
                        <p className="text-sm text-slate-400">{campaign.clicks.toLocaleString()} clicks</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-green-400">{campaign.rate}%</p>
                      <p className="text-sm text-slate-400">{campaign.conversions} conv.</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Device Breakdown */}
        <div className="bg-slate-800 border border-slate-700 rounded-lg">
          <div className="p-4 border-b border-slate-700">
            <h3 className="text-lg font-bold text-white">Device Breakdown</h3>
            <p className="text-sm text-slate-400">Traffic distribution by device type</p>
          </div>
          <div className="p-4">
            {devices.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-slate-400">No device data available</p>
                <p className="text-slate-500 text-sm">Data will appear as users visit your links</p>
              </div>
            ) : (
              <div className="space-y-3">
                {devices.map((device, index) => (
                  <div key={device.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: device.color }}
                      ></div>
                      <span className="text-white font-medium">{device.name}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-white font-bold">{device.value}%</span>
                      <p className="text-xs text-slate-400">{device.count} visits</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Geographic Distribution */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg">
        <div className="p-4 border-b border-slate-700">
          <h3 className="text-lg font-bold text-white">Geographic Distribution</h3>
          <p className="text-sm text-slate-400">Top countries by traffic volume</p>
        </div>
        <div className="p-4">
          {countries.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-slate-400">No geographic data available</p>
              <p className="text-slate-500 text-sm">Data will appear as users visit your links</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {countries.map((country) => (
                <div key={country.country} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{country.flag}</span>
                    <div>
                      <p className="font-medium text-white">{country.country}</p>
                      <p className="text-sm text-slate-400">{country.clicks} clicks</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-blue-400">{country.percentage}%</p>
                    <p className="text-xs text-slate-400">{country.visitors} visitors</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Analytics

