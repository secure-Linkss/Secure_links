'use client';

import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Users,
  FolderKanban,
  Shield,
  CreditCard,
  MessageSquare,
  FileText,
  Settings,
  LayoutDashboard,
  UserCheck,
  UserX,
  Trash2,
  Edit,
  Eye,
  MoreVertical,
  Download,
  RefreshCw,
  AlertTriangle,
  Plus,
  ChevronDown,
  ChevronUp,
  TrendingUp,
  Lock,
  Unlock,
  Mail,
  Phone,
  Globe,
  Activity,
  BarChart3,
  Zap,
  Copy,
  Trash,
  CheckCircle,
  AlertCircle,
  Clock,
  Server,
  Database,
  Shield as ShieldIcon,
  Key,
  X,
  Sliders,
} from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

// StatCard component for displaying metrics
const StatCard = ({ icon: Icon, label, value, color, onClick }) => (
  <Card className={`cursor-pointer hover:scale-105 transition-all duration-300 bg-slate-800 border-slate-700 ${onClick ? 'hover:bg-slate-700' : ''}`} onClick={onClick}>
    <CardContent className="p-4">
      <div className="flex items-center space-x-3">
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
        <div>
          <p className="text-lg font-bold text-white">{value}</p>
          <p className="text-xs text-slate-400">{label}</p>
        </div>
      </div>
    </CardContent>
  </Card>
);

export default function AdminPanelComplete() {
  // State management
  const [currentUser, setCurrentUser] = useState(null);
  
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        setCurrentUser(user);
      } catch (error) {
        console.error('Error parsing user data:', error);
      }
    }
  }, []);

  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [securityThreats, setSecurityThreats] = useState([]);
  const [supportTickets, setSupportTickets] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [activityLogs, setActivityLogs] = useState([]);
  const [pendingUsers, setPendingUsers] = useState([]);
  
  const [dashboardStats, setDashboardStats] = useState({
    totalUsers: 0,
    activeUsers: 0,
    pendingUsers: 0,
    suspendedUsers: 0,
    totalCampaigns: 0,
    activeCampaigns: 0,
    totalLinks: 0,
    totalClicks: 0,
    securityThreats: 0,
    supportTickets: 0,
    revenue: 0,
    conversionRate: 0
  });

  const [showUserDetailsDialog, setShowUserDetailsDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  // API functions
  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/admin/dashboard-stats', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setDashboardStats(data);
      } else {
        console.error('Failed to fetch dashboard stats');
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/admin/users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCampaigns = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/admin/campaigns', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setCampaigns(data);
      }
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPendingUsers = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/admin/pending-users', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setPendingUsers(data);
      }
    } catch (error) {
      console.error('Error fetching pending users:', error);
    } finally {
      setLoading(false);
    }
  };

  const approvePendingUser = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/admin/approve-user/${userId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        await fetchPendingUsers();
        await fetchDashboardStats();
      }
    } catch (error) {
      console.error('Error approving user:', error);
    }
  };

  const rejectPendingUser = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/admin/reject-user/${userId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        await fetchPendingUsers();
        await fetchDashboardStats();
      }
    } catch (error) {
      console.error('Error rejecting user:', error);
    }
  };

  const loadActivityLogs = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/admin/activity-logs', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setActivityLogs(data);
      }
    } catch (error) {
      console.error('Error fetching activity logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const showUserDetails = (user) => {
    setSelectedUser(user);
    setShowUserDetailsDialog(true);
  };

  // Load initial data
  useEffect(() => {
    fetchDashboardStats();
  }, []);

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'campaigns') {
      fetchCampaigns();
    } else if (activeTab === 'pending') {
      fetchPendingUsers();
    }
  }, [activeTab]);

  if (!currentUser || (currentUser.role !== "admin" && currentUser.role !== "main_admin")) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Access Denied</h1>
          <p className="text-slate-400">You don't have permission to access the admin panel.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="container mx-auto p-4 sm:p-6 lg:p-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold gradient-text">Admin Control Panel</h1>
              <p className="text-slate-400 text-sm sm:text-base">Comprehensive system management and analytics</p>
            </div>
            <div className="flex flex-col sm:flex-row gap-2 text-xs sm:text-sm">
              <Badge variant="secondary" className="bg-green-500/20 text-green-400">
                <Activity className="h-3 w-3 mr-1" />
                System Online
              </Badge>
              <Badge variant="outline" className="border-slate-600 text-slate-300">
                Welcome, {currentUser?.username}
              </Badge>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <div className="mb-6">
            <ScrollArea className="w-full">
              <TabsList className="inline-flex w-max bg-slate-800 p-2 rounded-lg">
                <TabsTrigger value="dashboard" className="text-xs sm:text-sm px-3 py-2">
                  <LayoutDashboard className="h-4 w-4 mr-1" />
                  Dashboard
                </TabsTrigger>
                <TabsTrigger value="users" className="text-xs sm:text-sm px-3 py-2">
                  <Users className="h-4 w-4 mr-1" />
                  Users
                </TabsTrigger>
                <TabsTrigger value="campaigns" className="text-xs sm:text-sm px-3 py-2">
                  <FolderKanban className="h-4 w-4 mr-1" />
                  Campaigns
                </TabsTrigger>
                <TabsTrigger value="security" className="text-xs sm:text-sm px-3 py-2">
                  <Shield className="h-4 w-4 mr-1" />
                  Security
                </TabsTrigger>
                <TabsTrigger value="subscriptions" className="text-xs sm:text-sm px-3 py-2">
                  <CreditCard className="h-4 w-4 mr-1" />
                  Subscriptions
                </TabsTrigger>
                <TabsTrigger value="support" className="text-xs sm:text-sm px-3 py-2">
                  <MessageSquare className="h-4 w-4 mr-1" />
                  Support
                </TabsTrigger>
                <TabsTrigger value="audit" className="text-xs sm:text-sm px-3 py-2">
                  <FileText className="h-4 w-4 mr-1" />
                  Audit
                </TabsTrigger>
                <TabsTrigger value="settings" className="text-xs sm:text-sm px-3 py-2">
                  <Settings className="h-4 w-4 mr-1" />
                  Settings
                </TabsTrigger>
                {currentUser?.role === "main_admin" && (
                  <>
                    <TabsTrigger value="crypto" className="text-xs sm:text-sm px-3 py-2">
                      <Key className="h-4 w-4 mr-1" />
                      Crypto
                    </TabsTrigger>
                    <TabsTrigger value="telegram" className="text-xs sm:text-sm px-3 py-2">
                      <MessageSquare className="h-4 w-4 mr-1" />
                      Telegram
                    </TabsTrigger>
                    <TabsTrigger value="broadcaster" className="text-xs sm:text-sm px-3 py-2">
                      <Activity className="h-4 w-4 mr-1" />
                      Broadcaster
                    </TabsTrigger>
                    <TabsTrigger value="pending" className="text-xs sm:text-sm px-3 py-2">
                      <Clock className="h-4 w-4 mr-1" />
                      Pending
                    </TabsTrigger>
                  </>
                )}
              </TabsList>
            </ScrollArea>
          </div>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">System Overview</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Real-time analytics and system metrics</p>
              </div>
              <Button onClick={fetchDashboardStats} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatCard icon={Users} label="Total Users" value={dashboardStats.totalUsers} color="bg-blue-500" />
              <StatCard icon={UserCheck} label="Active Users" value={dashboardStats.activeUsers} color="bg-green-500" />
              <StatCard icon={FolderKanban} label="Total Campaigns" value={dashboardStats.totalCampaigns} color="bg-purple-500" />
              <StatCard icon={BarChart3} label="Total Clicks" value={dashboardStats.totalClicks} color="bg-orange-500" />
              <StatCard icon={Shield} label="Security Threats" value={dashboardStats.securityThreats} color="bg-red-500" />
              <StatCard icon={MessageSquare} label="Support Tickets" value={dashboardStats.supportTickets} color="bg-yellow-500" />
              <StatCard icon={CreditCard} label="Revenue" value={`$${dashboardStats.revenue}`} color="bg-green-600" />
              <StatCard icon={TrendingUp} label="Conversion Rate" value={`${dashboardStats.conversionRate}%`} color="bg-indigo-500" />
            </div>

            {/* System Status Cards */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Server className="h-5 w-5 mr-2" />
                    System Health
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">API Status</span>
                      <Badge className="bg-green-500/20 text-green-400">Online</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Database</span>
                      <Badge className="bg-green-500/20 text-green-400">Connected</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Cache</span>
                      <Badge className="bg-green-500/20 text-green-400">Active</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Activity className="h-5 w-5 mr-2" />
                    Recent Activity
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="text-sm text-slate-400">
                      <div className="flex justify-between">
                        <span>New user registrations</span>
                        <span className="text-white">+12 today</span>
                      </div>
                    </div>
                    <div className="text-sm text-slate-400">
                      <div className="flex justify-between">
                        <span>Links created</span>
                        <span className="text-white">+247 today</span>
                      </div>
                    </div>
                    <div className="text-sm text-slate-400">
                      <div className="flex justify-between">
                        <span>Support tickets</span>
                        <span className="text-white">3 pending</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Users Tab */}
          <TabsContent value="users" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">User Management</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Manage all system users and their permissions</p>
              </div>
              <Button onClick={fetchUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
            </div>

            {/* User Management Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <StatCard icon={Users} label="Total Users" value={dashboardStats.totalUsers} color="bg-blue-500" />
              <StatCard icon={UserCheck} label="Active Users" value={dashboardStats.activeUsers} color="bg-green-500" />
              <StatCard icon={Clock} label="Pending Users" value={dashboardStats.pendingUsers} color="bg-yellow-500" />
              <StatCard icon={UserX} label="Suspended Users" value={dashboardStats.suspendedUsers} color="bg-red-500" />
            </div>

            {/* Users Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Users</CardTitle>
                <Button size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <Plus className="h-3 w-3 mr-1" />
                  Add User
                </Button>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="h-6 w-6 animate-spin text-slate-400" />
                  </div>
                ) : (
                  <ScrollArea className="h-96">
                    <Table>
                      <TableHeader>
                        <TableRow className="text-xs text-slate-400 border-slate-700">
                          <TableHead>User</TableHead>
                          <TableHead>Email</TableHead>
                          <TableHead>Role</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead>Created</TableHead>
                          <TableHead>Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {users.map((user) => (
                          <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                            <TableCell>
                              <div>
                                <div className="font-medium text-white">{user.username}</div>
                                <div className="text-xs text-slate-400">ID: {user.id}</div>
                              </div>
                            </TableCell>
                            <TableCell className="text-slate-300">{user.email}</TableCell>
                            <TableCell>
                              <Badge variant={user.role === 'admin' ? 'destructive' : 'secondary'}>
                                {user.role}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant={user.status === 'active' ? 'default' : 'destructive'}>
                                {user.status}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-400 text-xs">
                              {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                            </TableCell>
                            <TableCell>
                              <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                  <Button variant="ghost" className="h-8 w-8 p-0">
                                    <MoreVertical className="h-4 w-4" />
                                  </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700">
                                  <DropdownMenuItem onClick={() => showUserDetails(user)} className="text-slate-300 hover:bg-slate-700">
                                    <Eye className="h-4 w-4 mr-2" />
                                    View Details
                                  </DropdownMenuItem>
                                  <DropdownMenuItem className="text-slate-300 hover:bg-slate-700">
                                    <Edit className="h-4 w-4 mr-2" />
                                    Edit User
                                  </DropdownMenuItem>
                                  <DropdownMenuItem className="text-red-400 hover:bg-slate-700">
                                    <Trash2 className="h-4 w-4 mr-2" />
                                    Delete User
                                  </DropdownMenuItem>
                                </DropdownMenuContent>
                              </DropdownMenu>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </ScrollArea>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Campaigns Tab */}
          <TabsContent value="campaigns" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Campaign Management</h2>
                <p className="text-slate-400 text-xs sm:text-sm">View and manage all campaigns</p>
              </div>
              <Button onClick={fetchCampaigns} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
            </div>

            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-xl font-semibold">All Campaigns</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="h-6 w-6 animate-spin text-slate-400" />
                  </div>
                ) : (
                  <ScrollArea className="h-96">
                    <Table>
                      <TableHeader>
                        <TableRow className="text-xs text-slate-400 border-slate-700">
                          <TableHead>Campaign</TableHead>
                          <TableHead>Owner</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead>Links</TableHead>
                          <TableHead>Clicks</TableHead>
                          <TableHead>Created</TableHead>
                          <TableHead>Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {campaigns.map((campaign) => (
                          <TableRow key={campaign.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                            <TableCell>
                              <div className="font-medium text-white">{campaign.name}</div>
                            </TableCell>
                            <TableCell className="text-slate-300">{campaign.owner}</TableCell>
                            <TableCell>
                              <Badge variant={campaign.status === 'active' ? 'default' : 'secondary'}>
                                {campaign.status}
                              </Badge>
                            </TableCell>
                            <TableCell className="text-slate-300">{campaign.links_count || 0}</TableCell>
                            <TableCell className="text-slate-300">{campaign.clicks_count || 0}</TableCell>
                            <TableCell className="text-slate-400 text-xs">
                              {campaign.created_at ? new Date(campaign.created_at).toLocaleDateString() : 'N/A'}
                            </TableCell>
                            <TableCell>
                              <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                  <Button variant="ghost" className="h-8 w-8 p-0">
                                    <MoreVertical className="h-4 w-4" />
                                  </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end" className="bg-slate-800 border-slate-700">
                                  <DropdownMenuItem className="text-slate-300 hover:bg-slate-700">
                                    <Eye className="h-4 w-4 mr-2" />
                                    View Campaign
                                  </DropdownMenuItem>
                                  <DropdownMenuItem className="text-slate-300 hover:bg-slate-700">
                                    <Edit className="h-4 w-4 mr-2" />
                                    Edit Campaign
                                  </DropdownMenuItem>
                                </DropdownMenuContent>
                              </DropdownMenu>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </ScrollArea>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security Tab */}
          <TabsContent value="security" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Security Management</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Monitor and manage system security</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-lg">Security Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Firewall Status</span>
                      <Badge className="bg-green-500/20 text-green-400">Active</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">SSL Certificate</span>
                      <Badge className="bg-green-500/20 text-green-400">Valid</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Rate Limiting</span>
                      <Badge className="bg-green-500/20 text-green-400">Enabled</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-lg">Threat Detection</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Blocked IPs</span>
                      <span className="text-white font-semibold">0</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Failed Login Attempts</span>
                      <span className="text-white font-semibold">0</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-slate-400">Suspicious Activity</span>
                      <span className="text-white font-semibold">0</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Subscriptions Tab */}
          <TabsContent value="subscriptions" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Subscription Management</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Manage user subscriptions and billing</p>
              </div>
            </div>

            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-lg">Subscription Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <CreditCard className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                  <p className="text-slate-400">No subscription data available</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Support Tab */}
          <TabsContent value="support" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Support Management</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Handle customer support tickets</p>
              </div>
            </div>

            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-lg">Support Tickets</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <MessageSquare className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                  <p className="text-slate-400">No support tickets available</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Audit Tab */}
          <TabsContent value="audit" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Audit Logs</h2>
                <p className="text-slate-400 text-xs sm:text-sm">View system audit logs and user activity</p>
              </div>
              <Button onClick={loadActivityLogs} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
            </div>

            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-lg">Activity Logs</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400 border-slate-700">
                        <TableHead>Timestamp</TableHead>
                        <TableHead>User</TableHead>
                        <TableHead>Action</TableHead>
                        <TableHead>IP Address</TableHead>
                        <TableHead>Status</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {activityLogs.map((log, index) => (
                        <TableRow key={index} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell className="text-slate-400 text-xs">
                            {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'N/A'}
                          </TableCell>
                          <TableCell className="text-slate-300">{log.user || 'System'}</TableCell>
                          <TableCell className="text-slate-300">{log.action}</TableCell>
                          <TableCell className="text-slate-400">{log.ip_address || 'N/A'}</TableCell>
                          <TableCell>
                            <Badge variant={log.status === 'success' ? 'default' : 'destructive'}>
                              {log.status || 'completed'}
                            </Badge>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">System Settings</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Configure system-wide settings</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-lg">General Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="maintenance-mode" className="text-sm">Maintenance Mode</Label>
                    <Switch id="maintenance-mode" />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="user-registration" className="text-sm">User Registration</Label>
                    <Switch id="user-registration" defaultChecked />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="email-notifications" className="text-sm">Email Notifications</Label>
                    <Switch id="email-notifications" defaultChecked />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-lg">Security Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="two-factor" className="text-sm">Require 2FA</Label>
                    <Switch id="two-factor" />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="password-expiry" className="text-sm">Password Expiry</Label>
                    <Switch id="password-expiry" />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="session-timeout" className="text-sm">Session Timeout</Label>
                    <Switch id="session-timeout" defaultChecked />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Main Admin Only Tabs */}
          {currentUser?.role === "main_admin" && (
            <>
              {/* Crypto Tab */}
              <TabsContent value="crypto" className="space-y-6">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <h2 className="text-xl sm:text-2xl font-bold">Crypto Management</h2>
                    <p className="text-slate-400 text-xs sm:text-sm">Manage cryptocurrency payments and settings</p>
                  </div>
                </div>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-lg">Crypto Settings</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-8">
                      <Key className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                      <p className="text-slate-400">Crypto management features coming soon</p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Telegram Tab */}
              <TabsContent value="telegram" className="space-y-6">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <h2 className="text-xl sm:text-2xl font-bold">Telegram Integration</h2>
                    <p className="text-slate-400 text-xs sm:text-sm">Manage Telegram bot and notifications</p>
                  </div>
                </div>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-lg">Telegram Bot Status</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-8">
                      <MessageSquare className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                      <p className="text-slate-400">Telegram integration not configured</p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Broadcaster Tab */}
              <TabsContent value="broadcaster" className="space-y-6">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <h2 className="text-xl sm:text-2xl font-bold">Broadcaster Management</h2>
                    <p className="text-slate-400 text-xs sm:text-sm">Manage system broadcasts and notifications</p>
                  </div>
                </div>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-lg">Active Broadcasts</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center py-8">
                      <Activity className="h-12 w-12 mx-auto text-slate-400 mb-4" />
                      <p className="text-slate-400">No active broadcasts</p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* Pending Users Tab */}
              <TabsContent value="pending" className="space-y-6">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <h2 className="text-xl sm:text-2xl font-bold">Pending User Approvals</h2>
                    <p className="text-slate-400 text-xs sm:text-sm">Review and approve new user registrations</p>
                  </div>
                  <Button onClick={fetchPendingUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                    <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-lg">Pending Approvals</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {loading ? (
                      <div className="flex items-center justify-center py-8">
                        <RefreshCw className="h-6 w-6 animate-spin text-slate-400" />
                      </div>
                    ) : (
                      <ScrollArea className="h-96">
                        <Table>
                          <TableHeader>
                            <TableRow className="text-xs text-slate-400 border-slate-700">
                              <TableHead>Username</TableHead>
                              <TableHead>Email</TableHead>
                              <TableHead>Requested Role</TableHead>
                              <TableHead>Registration Date</TableHead>
                              <TableHead>Actions</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {pendingUsers.map((user) => (
                              <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                                <TableCell className="font-medium text-white">{user.username}</TableCell>
                                <TableCell className="text-slate-300">{user.email}</TableCell>
                                <TableCell>
                                  <Badge variant="secondary">{user.requested_role || 'user'}</Badge>
                                </TableCell>
                                <TableCell className="text-slate-400 text-xs">
                                  {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                                </TableCell>
                                <TableCell>
                                  <div className="flex gap-2">
                                    <Button
                                      size="sm"
                                      variant="default"
                                      onClick={() => approvePendingUser(user.id)}
                                      disabled={loading}
                                      className="bg-green-600 hover:bg-green-700"
                                    >
                                      <CheckCircle className="h-4 w-4 mr-1" />
                                      Approve
                                    </Button>
                                    <Button
                                      size="sm"
                                      variant="destructive"
                                      onClick={() => rejectPendingUser(user.id)}
                                      disabled={loading}
                                    >
                                      <X className="h-4 w-4 mr-1" />
                                      Reject
                                    </Button>
                                  </div>
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </ScrollArea>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
            </>
          )}
        </Tabs>
      </div>

      {/* User Details Dialog */}
      <Dialog open={showUserDetailsDialog} onOpenChange={setShowUserDetailsDialog}>
        <DialogContent className="bg-slate-800 border-slate-700 max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-white">User Details</DialogTitle>
            <DialogDescription className="text-slate-400">
              Comprehensive user information and activity
            </DialogDescription>
          </DialogHeader>
          {selectedUser && (
            <div className="space-y-4 text-white">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <Label className="text-slate-400 text-xs">Username</Label>
                  <p className="text-white font-medium">{selectedUser.username}</p>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Email</Label>
                  <p className="text-white font-medium">{selectedUser.email}</p>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Role</Label>
                  <Badge variant={selectedUser.role === 'admin' ? 'destructive' : 'secondary'}>
                    {selectedUser.role}
                  </Badge>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Status</Label>
                  <Badge variant={selectedUser.status === 'active' ? 'default' : 'destructive'}>
                    {selectedUser.status}
                  </Badge>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Created</Label>
                  <p className="text-white font-medium">
                    {selectedUser.created_at ? new Date(selectedUser.created_at).toLocaleString() : 'N/A'}
                  </p>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Last Login</Label>
                  <p className="text-white font-medium">
                    {selectedUser.last_login ? new Date(selectedUser.last_login).toLocaleString() : 'Never'}
                  </p>
                </div>
              </div>

              <div className="pt-4">
                <Label className="text-slate-400 text-xs">Additional Information</Label>
                <div className="mt-2 p-3 bg-slate-700 rounded">
                  <p className="text-sm text-slate-300">
                    User ID: {selectedUser.id}<br />
                    Email Verified: {selectedUser.is_verified ? 'Yes' : 'No'}<br />
                    Account Active: {selectedUser.is_active ? 'Yes' : 'No'}
                  </p>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}