import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select'
import { Badge } from './ui/badge'
import { Progress } from './ui/progress'
import {
  Globe,
  MapPin,
  Users,
  TrendingUp,
  RefreshCw,
  Download,
  Navigation
} from 'lucide-react'
import { 
  ComposableMap, 
  Geographies, 
  Geography as GeoComponent, 
  Marker 
} from 'react-simple-maps'

const geoUrl = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json"

const Geography = () => {
  const [timeRange, setTimeRange] = useState('7')
  const [loading, setLoading] = useState(true)
  const [geoData, setGeoData] = useState({
    countries: [],
    cities: [],
    totalCountries: 0,
    totalCities: 0,
    topCountry: null,
    topCity: null
  })
  const [mapData, setMapData] = useState({ geoData: [], totalLocations: 0 })

  useEffect(() => {
    fetchGeographyData()
  }, [timeRange])

  const fetchGeographyData = async () => {
    setLoading(true)
    try {
      // Fetch geography statistics
      const response = await fetch(`/api/analytics/geography?period=${timeRange}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setGeoData(data)
      }
      
      // Fetch map data with lat/lng coordinates
      const mapResponse = await fetch(`/api/analytics/geography/map-data?period=${timeRange}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (mapResponse.ok) {
        const data = await mapResponse.json()
        setMapData(data)
      }
    } catch (error) {
      console.error('Error fetching geography data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    fetchGeographyData()
  }

  const handleExport = () => {
    const csvData = [
      ['Country', 'Clicks', 'Percentage'],
      ...geoData.countries.map(c => [c.name, c.clicks, `${c.percentage}%`])
    ]
    
    const csvContent = csvData.map(row => row.join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `geography-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Geographic Analytics</h1>
        <p className="text-slate-400">Global traffic distribution and insights</p>
      </div>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger className="w-full sm:w-[180px] bg-slate-800 border-slate-700 text-white">
            <SelectValue placeholder="Select time range" />
          </SelectTrigger>
          <SelectContent className="bg-slate-800 border-slate-700">
            <SelectItem value="1">Last 24 hours</SelectItem>
            <SelectItem value="7">Last 7 days</SelectItem>
            <SelectItem value="30">Last 30 days</SelectItem>
            <SelectItem value="90">Last 90 days</SelectItem>
          </SelectContent>
        </Select>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleRefresh} className="border-slate-600 text-slate-300 hover:bg-slate-700">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline" size="sm" onClick={handleExport} className="border-slate-600 text-slate-300 hover:bg-slate-700">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Stat Cards - 4 cards in one row - Mobile: 2 cols, Desktop: 4 cols */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <Card className="bg-gradient-to-br from-blue-500/10 to-blue-600/5 border-blue-500/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-400 mb-1">Total Countries</p>
                <p className="text-3xl font-bold text-white">{geoData.totalCountries}</p>
              </div>
              <div className="p-3 bg-blue-500/20 rounded-full">
                <Globe className="h-6 w-6 text-blue-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-500/10 to-green-600/5 border-green-500/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-400 mb-1">Total Cities</p>
                <p className="text-3xl font-bold text-white">{geoData.totalCities}</p>
              </div>
              <div className="p-3 bg-green-500/20 rounded-full">
                <MapPin className="h-6 w-6 text-green-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-500/10 to-purple-600/5 border-purple-500/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-400 mb-1">Top Country</p>
                <p className="text-xl font-bold text-white truncate">
                  {geoData.topCountry ? `${geoData.topCountry.flag} ${geoData.topCountry.name}` : 'N/A'}
                </p>
              </div>
              <div className="p-3 bg-purple-500/20 rounded-full">
                <TrendingUp className="h-6 w-6 text-purple-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-500/10 to-orange-600/5 border-orange-500/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-400 mb-1">Top City</p>
                <p className="text-xl font-bold text-white truncate">
                  {geoData.topCity ? geoData.topCity.name : 'N/A'}
                </p>
              </div>
              <div className="p-3 bg-orange-500/20 rounded-full">
                <Navigation className="h-6 w-6 text-orange-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Map and Data Grid - Mobile: 1 col, Desktop: 2 cols */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Interactive World Map */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-semibold">Traffic Heat Map</CardTitle>
            <CardDescription>Global visitor distribution</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="w-full h-[400px] bg-slate-800/50 rounded-lg flex items-center justify-center">
              <ComposableMap
                projection="geoMercator"
                projectionConfig={{
                  scale: 100
                }}
              >
                <Geographies geography={geoUrl}>
                  {({ geographies }) =>
                    geographies.map((geo) => {
                      const country = geoData.countries.find(c => c.name === geo.properties.name)
                      return (
                        <GeoComponent
                          key={geo.rsmKey}
                          geography={geo}
                          fill={country ? `rgba(59, 130, 246, ${Math.min(country.percentage / 50, 1)})` : "#1e293b"}
                          stroke="#475569"
                          strokeWidth={0.5}
                          style={{
                            hover: {
                              fill: "#3b82f6",
                              outline: "none"
                            }
                          }}
                        />
                      )
                    })
                  }
                </Geographies>
                
                {/* Add markers for locations with lat/lng data */}
                {mapData.geoData && mapData.geoData.map((location, index) => (
                  <Marker key={index} coordinates={[location.lng, location.lat]}>
                    <circle 
                      r={Math.min(4 + (location.clicks * 0.5), 12)} 
                      fill="#ef4444" 
                      stroke="#fff" 
                      strokeWidth={1.5}
                      opacity={0.8}
                    />
                    <title>{`${location.city}, ${location.country}: ${location.clicks} clicks`}</title>
                  </Marker>
                ))}
              </ComposableMap>
            </div>
          </CardContent>
        </Card>

        {/* Top Countries List */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-semibold">Top Countries</CardTitle>
            <CardDescription>Highest traffic sources</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-[400px] overflow-y-auto">
              {geoData.countries.slice(0, 10).map((country, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg hover:bg-slate-800 transition-colors">
                  <div className="flex items-center gap-3 flex-1">
                    <span className="text-2xl">{country.flag}</span>
                    <div className="flex-1">
                      <p className="font-medium text-white">{country.name}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <Progress value={country.percentage} className="h-2 flex-1" />
                        <span className="text-xs text-slate-400 w-12 text-right">{country.percentage}%</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <p className="text-sm font-semibold text-white">{country.clicks.toLocaleString()}</p>
                    <p className="text-xs text-slate-400">clicks</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Cities Table */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base font-semibold">Top Cities</CardTitle>
          <CardDescription>Most active urban locations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {geoData.cities.slice(0, 10).map((city, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-800/30 rounded-lg hover:bg-slate-800/50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <MapPin className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <p className="font-medium text-white">{city.name}</p>
                    <p className="text-sm text-slate-400">{city.country}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-white">{city.clicks.toLocaleString()}</p>
                  <p className="text-xs text-slate-400">clicks</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Geography
