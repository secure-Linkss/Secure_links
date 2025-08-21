import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { 
  Link2, 
  Plus, 
  Copy, 
  Edit, 
  Trash2, 
  ExternalLink,
  RefreshCw,
  Search,
  Filter,
  MoreHorizontal
} from 'lucide-react'

export default function LinksTab() {
  const [links, setLinks] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [newLink, setNewLink] = useState({
    target_url: '',
    title: '',
    campaign_id: null
  })

  useEffect(() => {
    fetchLinks()
  }, [])

  const fetchLinks = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/links', {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setLinks(data)
      }
    } catch (error) {
      console.error('Failed to fetch links:', error)
    } finally {
      setLoading(false)
    }
  }

  const createLink = async () => {
    try {
      const response = await fetch('/api/links', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(newLink),
      })
      
      if (response.ok) {
        setShowCreateDialog(false)
        setNewLink({ target_url: '', title: '', campaign_id: null })
        fetchLinks()
      }
    } catch (error) {
      console.error('Failed to create link:', error)
    }
  }

  const copyToClipboard = (shortCode) => {
    const url = `${window.location.origin}/t/${shortCode}`
    navigator.clipboard.writeText(url)
  }

  const filteredLinks = links.filter(link =>
    link.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    link.target_url.toLowerCase().includes(searchTerm.toLowerCase()) ||
    link.short_code.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="space-y-4 md:space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl md:text-3xl font-bold">Tracking Links</h1>
          <RefreshCw className="h-5 w-5 animate-spin" />
        </div>
        <div className="grid grid-cols-1 gap-4">
          {[...Array(5)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-4 md:p-6">
                <div className="h-20 bg-muted rounded"></div>
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
            <Link2 className="h-6 w-6 md:h-8 md:w-8 text-green-500" />
            Tracking Links
          </h1>
          <p className="text-sm md:text-base text-muted-foreground">Create and manage your tracking links</p>
        </div>
        
        <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
          <DialogTrigger asChild>
            <Button className="w-full sm:w-auto">
              <Plus className="h-4 w-4 mr-2" />
              Create Link
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Create New Link</DialogTitle>
              <DialogDescription>
                Generate a new tracking link for your campaign
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="target_url">Target URL</Label>
                <Input
                  id="target_url"
                  placeholder="https://example.com"
                  value={newLink.target_url}
                  onChange={(e) => setNewLink({...newLink, target_url: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="title">Title (Optional)</Label>
                <Input
                  id="title"
                  placeholder="Link description"
                  value={newLink.title}
                  onChange={(e) => setNewLink({...newLink, title: e.target.value})}
                />
              </div>
              <Button onClick={createLink} className="w-full">
                Create Link
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search links..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline" size="sm">
          <Filter className="h-4 w-4 mr-2" />
          Filter
        </Button>
        <Button variant="outline" size="sm" onClick={fetchLinks}>
          <RefreshCw className="h-4 w-4" />
        </Button>
      </div>

      {/* Links List */}
      <div className="space-y-4">
        {filteredLinks.length > 0 ? (
          filteredLinks.map((link) => (
            <Card key={link.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-4 md:p-6">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                      <h3 className="font-semibold text-sm md:text-base truncate">
                        {link.title || 'Untitled Link'}
                      </h3>
                      <div className="flex items-center gap-2">
                        <Badge variant="secondary" className="text-xs">
                          {link.short_code}
                        </Badge>
                        {link.campaign_name && (
                          <Badge variant="outline" className="text-xs">
                            {link.campaign_name}
                          </Badge>
                        )}
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-xs md:text-sm text-muted-foreground">
                        <ExternalLink className="h-3 w-3 md:h-4 md:w-4" />
                        <span className="truncate">{link.target_url}</span>
                      </div>
                      
                      <div className="flex items-center gap-2 text-xs md:text-sm">
                        <Link2 className="h-3 w-3 md:h-4 md:w-4 text-blue-500" />
                        <code className="bg-muted px-2 py-1 rounded text-xs">
                          {window.location.origin}/t/{link.short_code}
                        </code>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(link.short_code)}
                          className="h-6 w-6 p-0"
                        >
                          <Copy className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                    {/* Stats */}
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <p className="text-lg md:text-xl font-bold">{link.total_clicks}</p>
                        <p className="text-xs text-muted-foreground">Clicks</p>
                      </div>
                      <div>
                        <p className="text-lg md:text-xl font-bold">{link.real_visitors}</p>
                        <p className="text-xs text-muted-foreground">Visitors</p>
                      </div>
                      <div>
                        <p className="text-lg md:text-xl font-bold">{link.blocked_attempts}</p>
                        <p className="text-xs text-muted-foreground">Blocked</p>
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex items-center gap-2">
                      <Button variant="ghost" size="sm">
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <Card>
            <CardContent className="p-8 md:p-12 text-center">
              <Link2 className="h-12 w-12 md:h-16 md:w-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg md:text-xl font-semibold mb-2">No links found</h3>
              <p className="text-sm md:text-base text-muted-foreground mb-4">
                {searchTerm ? 'No links match your search criteria.' : 'Create your first tracking link to get started.'}
              </p>
              {!searchTerm && (
                <Button onClick={() => setShowCreateDialog(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Create Your First Link
                </Button>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

