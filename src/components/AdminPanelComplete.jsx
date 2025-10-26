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
  Sliders,
  Search,
  Filter,
  X,
  Check,
  ExternalLink,
  Calendar,
  User,
  Star,
  Info,
  AlertTriangle as Warning,
  Home,
  Settings2,
  Save,
  Upload,
  DollarSign,
  CreditCard as CardIcon,
  AlertOctagon,
  Wrench,
  MonitorSpeaker,
  PieChart as PieChartIcon,
  Link2,
  Ban,
  Send,
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
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';

export default function AdminPanelComplete() {
  // Get current user from localStorage
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setCurrentUser(JSON.parse(userData));
    }
  }, []);

  const isMainAdmin = currentUser?.role === 'main_admin';
  const isAdmin = currentUser?.role === 'admin' || currentUser?.role === 'main_admin';

  // State management
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Data state
  const [dashboardStats, setDashboardStats] = useState({
    totalUsers: 0,
    activeUsers: 0,
    pendingUsers: 0,
    suspendedUsers: 0,
    adminCount: 0,
    totalUsers: 0,
    totalLinks: 0,
    totalClicks: 0,
    totalCampaigns: 0,
    activeUsers: 0,
    activeCampaigns: 0,
    activeLinks: 0,
    newUsersToday: 0,
    securityThreats: 0,
    openTickets: 0,
  });

  const [users, setUsers] = useState([]);
  const [pendingUsers, setPendingUsers] = useState([]);
  const [suspendedUsers, setSuspendedUsers] = useState([]);
  const [activityLogs, setActivityLogs] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [securityThreats, setSecurityThreats] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [supportTickets, setSupportTickets] = useState([]);
  const [domains, setDomains] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [broadcastMessage, setBroadcastMessage] = useState('');
  const [telegramBots, setTelegramBots] = useState([]);
  const [cryptoPayments, setCryptoPayments] = useState([]);
  const [telegramSettings, setTelegramSettings] = useState({
    botToken: '',
    chatId: '',
    status: 'disconnected', // 'connected', 'disconnected', 'testing'
  });

  // Dialog states
  const [showCreateUserDialog, setShowCreateUserDialog] = useState(false);
  const [showEditUserDialog, setShowEditUserDialog] = useState(false);
  const [showCreateDomainDialog, setShowCreateDomainDialog] = useState(false);
  const [showUserDetailsDialog, setShowUserDetailsDialog] = useState(false);
  const [showCampaignDetailsDialog, setShowCampaignDetailsDialog] = useState(false);
  const [showTicketDetailsDialog, setShowTicketDetailsDialog] = useState(false);
  const [showDomainSettingsDialog, setShowDomainSettingsDialog] = useState(false);
  const [systemDeleteDialog, setSystemDeleteDialog] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  // Form states
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    password: '',
    role: 'member',
    status: 'active',
    plan_type: 'free',
    is_active: true,
    is_verified: false,
  });

  const [newDomain, setNewDomain] = useState({
    domain: '',
    domain_type: 'custom',
    description: '',
    is_active: true,
    api_key: '',
    api_secret: '',
  });

  const [selectedUser, setSelectedUser] = useState(null);
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState(null);
  const [expandedCampaignId, setExpandedCampaignId] = useState(null);
  const [confirmText, setConfirmText] = useState('');

  // Utility functions
  const getAuthHeaders = () => ({
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
    'Content-Type': 'application/json',
  });

  const showError = (message) => {
    setError(message);
    setTimeout(() => setError(null), 5000);
  };

  const showSuccess = (message) => {
    setSuccess(message);
    setTimeout(() => setSuccess(null), 5000);
  };

  // API calls
  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/dashboard', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setDashboardStats(data);
      } else {
        // Fallback to dashboard/stats endpoint
        const fallbackResponse = await fetch('/api/admin/dashboard/stats', {
          headers: getAuthHeaders()
        });
        if (fallbackResponse.ok) {
          const data = await fallbackResponse.json();
          setDashboardStats({
            totalUsers: data.users?.total || 0,
            totalLinks: data.links?.total || 0,
            totalClicks: data.clicks?.total || 0,
            totalCampaigns: data.campaigns?.total || 0,
            activeUsers: data.users?.active || 0,
            activeCampaigns: data.campaigns?.active || 0,
            activeLinks: data.links?.active || 0,
            newUsersToday: data.users?.new_today || 0,
            securityThreats: 0,
            openTickets: 0,
          });
        }
      }
    } catch (error) {
      console.error('Failed to load dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/users', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setUsers(Array.isArray(data) ? data : data.users || []);
      } else {
        showError('Failed to load users');
      }
    } catch (error) {
      showError('Error loading users');
    } finally {
      setLoading(false);
    }
  };

  const loadPendingUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/users/pending', {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setPendingUsers(Array.isArray(data) ? data : data.users || []);
      } else {
        showError('Failed to load pending users');
      }
    } catch (error) {
      showError('Error loading pending users');
    } finally {
      setLoading(false);
    }
  };

  const loadSuspendedUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/users/suspended', {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setSuspendedUsers(Array.isArray(data) ? data : data.users || []);
      } else {
        showError('Failed to load suspended users');
      }
    } catch (error) {
      showError('Error loading suspended users');
    } finally {
      setLoading(false);
    }
  };

  const loadActivityLogs = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/activity-logs', {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setActivityLogs(Array.isArray(data) ? data : data.logs || []);
      } else {
        showError('Failed to load activity logs');
      }
    } catch (error) {
      showError('Error loading activity logs');
    } finally {
      setLoading(false);
    }
  };

  const loadCampaigns = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/campaigns', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setCampaigns(Array.isArray(data) ? data : data.campaigns || []);
      } else {
        showError('Failed to load campaigns');
      }
    } catch (error) {
      showError('Error loading campaigns');
    } finally {
      setLoading(false);
    }
  };

  const loadSecurityThreats = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/security/threats', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setSecurityThreats(Array.isArray(data) ? data : data.threats || []);
      } else {
        showError('Failed to load security threats');
      }
    } catch (error) {
      showError('Error loading security threats');
    } finally {
      setLoading(false);
    }
  };

  const loadSubscriptions = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/subscriptions', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setSubscriptions(Array.isArray(data) ? data : data.subscriptions || []);
      } else {
        showError('Failed to load subscriptions');
      }
    } catch (error) {
      showError('Error loading subscriptions');
    } finally {
      setLoading(false);
    }
  };

  const loadSupportTickets = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/support/tickets', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setSupportTickets(Array.isArray(data) ? data : data.tickets || []);
      } else {
        showError('Failed to load support tickets');
      }
    } catch (error) {
      showError('Error loading support tickets');
    } finally {
      setLoading(false);
    }
  };

  const loadAuditLogs = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/audit-logs', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setAuditLogs(Array.isArray(data) ? data : data.logs || []);
      } else {
        showError('Failed to load audit logs');
      }
    } catch (error) {
      showError('Error loading audit logs');
    } finally {
      setLoading(false);
    }
  };

  const loadDomains = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/domains', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setDomains(Array.isArray(data) ? data : data.domains || []);
      } else {
        showError('Failed to load domains');
      }
    } catch (error) {
      showError('Error loading domains');
    } finally {
      setLoading(false);
    }
  };

  // CRUD operations
  const createUser = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/users', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(newUser)
      });

      if (response.ok) {
        showSuccess('User created successfully');
        setShowCreateUserDialog(false);
        setNewUser({
          username: '',
          email: '',
          password: '',
          role: 'member',
          status: 'active',
          plan_type: 'free',
          is_active: true,
          is_verified: false,
        });
        loadUsers();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to create user');
      }
    } catch (error) {
      showError('Error creating user');
    } finally {
      setLoading(false);
    }
  };

  const createDomain = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/domains', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(newDomain)
      });

      if (response.ok) {
        showSuccess('Domain created successfully');
        setShowCreateDomainDialog(false);
        setNewDomain({
          domain: '',
          domain_type: 'custom',
          description: '',
          is_active: true,
          api_key: '',
          api_secret: '',
        });
        loadDomains();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to create domain');
      }
    } catch (error) {
      showError('Error creating domain');
    } finally {
      setLoading(false);
    }
  };

  const deleteUser = async (userId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/admin/users/${userId}/delete`, {
        method: 'POST',
        headers: getAuthHeaders()
      });

      if (response.ok) {
        showSuccess('User deleted successfully');
        loadUsers();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to delete user');
      }
    } catch (error) {
      showError('Error deleting user');
    } finally {
      setLoading(false);
    }
  };

  const updateUser = async (userId, updates) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(updates)
      });

      if (response.ok) {
        showSuccess('User updated successfully');
        loadUsers();
        return true;
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to update user');
        return false;
      }
    } catch (error) {
      showError('Error updating user');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const resetUserPassword = async (userId) => {
    const newPassword = prompt('Enter new password for this user:');
    if (!newPassword) return;

    if (newPassword.length < 8) {
      showError('Password must be at least 8 characters');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`/api/admin/users/${userId}/reset-password`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ new_password: newPassword })
      });

      if (response.ok) {
        showSuccess('Password reset successfully');
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to reset password');
      }
    } catch (error) {
      showError('Error resetting password');
    } finally {
      setLoading(false);
    }
  };

  const toggleUserStatus = async (userId, currentStatus) => {
    const newStatus = currentStatus === 'active' ? 'suspended' : 'active';
    await updateUser(userId, { status: newStatus });
  };

  const deleteDomain = async (domainId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/admin/domains/${domainId}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      });

      if (response.ok) {
        showSuccess('Domain deleted successfully');
        loadDomains();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to delete domain');
      }
    } catch (error) {
      showError('Error deleting domain');
    } finally {
      setLoading(false);
    }
  };

  const loadTelegramSettings = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/settings/telegram', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const data = await response.json();
        setTelegramSettings({
          botToken: data.bot_token || '',
          chatId: data.chat_id || '',
          status: data.status || 'disconnected',
        });
      } else {
        showError('Failed to load Telegram settings');
      }
    } catch (error) {
      showError('Error loading Telegram settings');
    } finally {
      setLoading(false);
    }
  };

  const saveTelegramSettings = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/admin/settings/telegram', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ 
          bot_token: telegramSettings.botToken,
          chat_id: telegramSettings.chatId,
        })
      });

      if (response.ok) {
        const data = await response.json();
        setTelegramSettings(prev => ({ ...prev, status: data.status || 'connected' }));
        showSuccess('Telegram settings saved successfully');
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to save Telegram settings');
      }
    } catch (error) {
      showError('Error saving Telegram settings');
    } finally {
      setLoading(false);
    }
  };

  const testTelegramConnection = async () => {
    try {
      setLoading(true);
      setTelegramSettings(prev => ({ ...prev, status: 'testing' }));
      const response = await fetch('/api/admin/settings/telegram/test', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ 
          bot_token: telegramSettings.botToken,
          chat_id: telegramSettings.chatId,
        })
      });

      if (response.ok) {
        const data = await response.json();
        setTelegramSettings(prev => ({ ...prev, status: data.status || 'connected' }));
        showSuccess('Test message sent successfully! Status: ' + (data.status || 'connected'));
      } else {
        setTelegramSettings(prev => ({ ...prev, status: 'disconnected' }));
        const data = await response.json();
        showError(data.error || 'Test failed. Check your token and chat ID.');
      }
    } catch (error) {
      setTelegramSettings(prev => ({ ...prev, status: 'disconnected' }));
      showError('Error testing Telegram connection');
    } finally {
      setLoading(false);
    }
  };

  const toggleCampaignExpansion = (campaignId) => {
    setExpandedCampaignId(expandedCampaignId === campaignId ? null : campaignId);
  };

  const exportAuditLogs = async () => {
    try {
      const response = await fetch('/api/admin/audit-logs/export', {
        headers: getAuthHeaders()
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `audit_logs_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        showSuccess('Audit logs exported successfully');
      } else {
        showError('Failed to export audit logs');
      }
    } catch (error) {
      showError('Error exporting audit logs');
    }
  };

  const deleteAllSystemData = async () => {
    if (confirmText !== 'DELETE ALL DATA') {
      showError('Please type "DELETE ALL DATA" to confirm');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/admin/system/delete-all', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ confirm: 'DELETE_ALL_DATA' })
      });

      if (response.ok) {
        showSuccess('All system data deleted successfully');
        setSystemDeleteDialog(false);
        setConfirmText('');
        loadDashboardStats();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to delete system data');
      }
    } catch (error) {
      showError('Error deleting system data');
    } finally {
      setLoading(false);
    }
  };



  const approvePendingUser = async (userId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/pending-users/${userId}/approve`, {
        method: 'POST',
        headers: getAuthHeaders()
      });

      if (response.ok) {
        showSuccess('User approved successfully');
        loadPendingUsers();
        loadUsers();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to approve user');
      }
    } catch (error) {
      showError('Error approving user');
    } finally {
      setLoading(false);
    }
  };

  const rejectPendingUser = async (userId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/pending-users/${userId}/reject`, {
        method: 'POST',
        headers: getAuthHeaders()
      });

      if (response.ok) {
        showSuccess('User rejected successfully');
        loadPendingUsers();
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to reject user');
      }
    } catch (error) {
      showError('Error rejecting user');
    } finally {
      setLoading(false);
    }
  };

  // Broadcaster API functions
  const [broadcastForm, setBroadcastForm] = useState({
    title: '',
    message: '',
    type: 'info',
    priority: 'medium'
  });

  const sendBroadcast = async () => {
    if (!broadcastForm.title || !broadcastForm.message) {
      showError('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('/api/broadcaster/send', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(broadcastForm)
      });

      if (response.ok) {
        const data = await response.json();
        showSuccess(data.message);
        setBroadcastForm({
          title: '',
          message: '',
          type: 'info',
          priority: 'medium'
        });
      } else {
        const data = await response.json();
        showError(data.error || 'Failed to send broadcast');
      }
    } catch (error) {
      showError('Error sending broadcast');
    } finally {
      setLoading(false);
    }
  };

  // Utility functions
  const getStatusBadge = (status) => {
    const colorMap = {
      'pending': 'bg-yellow-500 text-yellow-50',
      'active': 'bg-green-500 text-green-50',
      'suspended': 'bg-red-500 text-red-50',
      'expired': 'bg-orange-500 text-orange-50',
      'verified': 'bg-blue-500 text-blue-50',
      'open': 'bg-yellow-500 text-yellow-50',
      'in_progress': 'bg-blue-500 text-blue-50',
      'closed': 'bg-green-500 text-green-50',
      'resolved': 'bg-green-500 text-green-50',
      'inactive': 'bg-gray-500 text-gray-50',
      'member': 'bg-blue-500 text-blue-50',
      'admin': 'bg-purple-500 text-purple-50',
      'main_admin': 'bg-red-500 text-red-50',
      'free': 'bg-gray-500 text-gray-50',
      'pro': 'bg-blue-500 text-blue-50',
      'enterprise': 'bg-purple-500 text-purple-50',
      'low': 'bg-green-500 text-green-50',
      'medium': 'bg-yellow-500 text-yellow-50',
      'high': 'bg-orange-500 text-orange-50',
      'critical': 'bg-red-500 text-red-50',
    };
    
    return (
      <Badge className={`${colorMap[status] || 'bg-gray-500 text-gray-50'} text-xs px-2 py-1`}>
        {status}
      </Badge>
    );
  };

  const StatCard = ({ icon: Icon, label, value, color, subtitle }) => (
    <Card className="bg-slate-800 border-slate-700 hover:bg-slate-750 transition-colors">
      <CardContent className="p-4 sm:p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <p className="text-slate-400 text-xs sm:text-sm font-medium">{label}</p>
            <p className="text-2xl sm:text-3xl font-bold text-white mt-1">{value}</p>
            {subtitle && (
              <p className="text-slate-500 text-xs mt-1">{subtitle}</p>
            )}
          </div>
          <div className={`p-2 sm:p-3 rounded-lg ${color} flex-shrink-0`}>
            <Icon className="h-5 w-5 sm:h-6 sm:w-6 text-white" />
          </div>
        </div>
      </CardContent>
    </Card>
  );

  // Effects
  useEffect(() => {
    loadDashboardStats();
    const interval = setInterval(() => {
      if (autoRefresh) {
        loadDashboardStats();
      }
    }, 30000);
    return () => clearInterval(interval);
  }, [autoRefresh]);

  useEffect(() => {
    switch (activeTab) {
      case 'users':
        loadUsers();
        break;
      case 'campaigns':
        loadCampaigns();
        break;
      case 'security':
        loadSecurityThreats();
        break;
      case 'subscriptions':
        loadSubscriptions();
        break;
      case 'support':
        loadSupportTickets();
        break;
       case 'audit':
        loadAuditLogs();
        break;
      case 'settings':
        loadDomains();
        loadTelegramSettings(); // Load Telegram settings on entering the settings tab
        break;
      default:
        break;
    }
  }, [activeTab]);

  // Filter functions
  const filteredUsers = users.filter(user => {
    const matchesSearch = user.username?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.email?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || user.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || campaign.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="w-full min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-slate-950/95 backdrop-blur-sm border-b border-slate-800 p-4 sm:p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl sm:text-4xl font-bold">Admin Panel</h1>
            <p className="text-slate-400 text-sm sm:text-base">Enterprise-grade administration dashboard</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-green-500" />
              <span className="text-xs text-slate-400">System Online</span>
            </div>
            <Button
              onClick={loadDashboardStats}
              variant="outline"
              size="sm"
              disabled={loading}
              className="text-xs sm:text-sm"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
        </div>
      </div>

      {/* Error/Success Notifications */}
      {error && (
        <div className="mx-4 sm:mx-6 mt-4 p-3 sm:p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-200 text-xs sm:text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
          <Button onClick={() => setError(null)} variant="ghost" size="sm" className="text-red-100 hover:text-red-50">
            <X className="h-4 w-4" />
          </Button>
        </div>
      )}

      {success && (
        <div className="mx-4 sm:mx-6 mt-4 p-3 sm:p-4 bg-green-500/20 border border-green-500 rounded-lg text-green-200 text-xs sm:text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle className="h-4 w-4 flex-shrink-0" />
            <span>{success}</span>
          </div>
          <Button onClick={() => setSuccess(null)} variant="ghost" size="sm" className="text-green-100 hover:text-green-50">
            <X className="h-4 w-4" />
          </Button>
        </div>
      )}

      {/* Main Content */}
      <div className="p-4 sm:p-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          {/* Tab Navigation */}
          <div className="mb-6">
            <ScrollArea className="w-full whitespace-nowrap">
              <TabsList className="inline-flex w-max bg-slate-800 p-2 rounded-lg">
                <TabsTrigger value="dashboard" className="text-xs sm:text-sm px-3 py-2">
                  <LayoutDashboard className="h-4 w-4 mr-2" />
                  <span className="hidden sm:inline">Dashboard</span>
                  <span className="sm:hidden">Dash</span>
                </TabsTrigger>
                <TabsTrigger value="users" className="text-xs sm:text-sm px-3 py-2">
                  <Users className="h-4 w-4 mr-2" />
                  Users
                </TabsTrigger>
                <TabsTrigger value="campaigns" className="text-xs sm:text-sm px-3 py-2">
                  <FolderKanban className="h-4 w-4 mr-2" />
                  <span className="hidden sm:inline">Campaigns</span>
                  <span className="sm:hidden">Camp</span>
                </TabsTrigger>
                <TabsTrigger value="security" className="text-xs sm:text-sm px-3 py-2">
                  <Shield className="h-4 w-4 mr-2" />
                  <span className="hidden sm:inline">Security</span>
                  <span className="sm:hidden">Sec</span>
                </TabsTrigger>
                <TabsTrigger value="subscriptions" className="text-xs sm:text-sm px-3 py-2">
                  <CreditCard className="h-4 w-4 mr-2" />
                  <span className="hidden sm:inline">Subscriptions</span>
                  <span className="sm:hidden">Subs</span>
                </TabsTrigger>
                <TabsTrigger value="support" className="text-xs sm:text-sm px-3 py-2">
                  <MessageSquare className="h-4 w-4 mr-2" />
                  <span className="hidden sm:inline">Support</span>
                  <span className="sm:hidden">Supp</span>
                </TabsTrigger>
                <TabsTrigger value="audit" className="text-xs sm:text-sm px-3 py-2">
                  <FileText className="h-4 w-4 mr-2" />
                  Audit
                </TabsTrigger>
                <TabsTrigger value="settings" className="text-xs sm:text-sm px-3 py-2">
                  <Settings className="h-4 w-4 mr-2" />
                  <span className="hidden sm:inline">Settings</span>
                  <span className="sm:hidden">Set</span>
                </TabsTrigger>
                {isMainAdmin && (
                  <TabsTrigger value="crypto" className="text-xs sm:text-sm px-3 py-2">
                    <DollarSign className="h-4 w-4 mr-2" />
                    <span className="hidden sm:inline">Crypto Payments</span>
                    <span className="sm:hidden">Crypto</span>
                  </TabsTrigger>
                )}
                {isMainAdmin && (
                  <TabsTrigger value="telegram" className="text-xs sm:text-sm px-3 py-2">
                    <MonitorSpeaker className="h-4 w-4 mr-2" />
                    <span className="hidden sm:inline">System Telegram</span>
                    <span className="sm:hidden">Sys-TG</span>
                  </TabsTrigger>
                )}
                {isAdmin && (
                  <TabsTrigger value="broadcaster" className="text-xs sm:text-sm px-3 py-2">
                    <MonitorSpeaker className="h-4 w-4 mr-2" />
                    <span className="hidden sm:inline">Broadcaster</span>
                    <span className="sm:hidden">Broad</span>
                  </TabsTrigger>
                )}
                {isAdmin && (
                  <TabsTrigger value="pending" className="text-xs sm:text-sm px-3 py-2">
                    <Clock className="h-4 w-4 mr-2" />
                    <span className="hidden sm:inline">Pending Users</span>
                    <span className="sm:hidden">Pending</span>
                  </TabsTrigger>
                )}
              </TabsList>
            </ScrollArea>
          </div>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Dashboard Overview</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Real-time system metrics and statistics</p>
              </div>
              <div className="flex items-center gap-3 w-full sm:w-auto">
                <div className="flex items-center gap-2">
                  <label className="text-xs sm:text-sm text-slate-400">Auto-refresh</label>
                  <Switch
                    checked={autoRefresh}
                    onCheckedChange={setAutoRefresh}
                  />
                </div>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
              <StatCard 
                icon={Users} 
                label="Total Users" 
                value={dashboardStats.totalUsers} 
                color="bg-blue-500" 
                subtitle={`${dashboardStats.activeUsers} active`}
              />
              <StatCard 
                icon={FolderKanban} 
                label="Total Campaigns" 
                value={dashboardStats.totalCampaigns} 
                color="bg-purple-500" 
                subtitle={`${dashboardStats.activeCampaigns} active`}
              />
              <StatCard 
                icon={TrendingUp} 
                label="Total Links" 
                value={dashboardStats.totalLinks} 
                color="bg-green-500" 
                subtitle={`${dashboardStats.activeLinks} active`}
              />
              <StatCard 
                icon={Activity} 
                label="Total Clicks" 
                value={dashboardStats.totalClicks} 
                color="bg-orange-500" 
              />
            </div>

            {/* Additional Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
              <StatCard 
                icon={UserCheck} 
                label="New Users Today" 
                value={dashboardStats.newUsersToday} 
                color="bg-cyan-500" 
              />
              <StatCard 
                icon={Shield} 
                label="Security Threats" 
                value={dashboardStats.securityThreats} 
                color="bg-red-500" 
              />
              <StatCard 
                icon={MessageSquare} 
                label="Open Tickets" 
                value={dashboardStats.openTickets} 
                color="bg-yellow-500" 
              />
            </div>

            {/* System Health */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-lg sm:text-xl flex items-center gap-2">
                  <Server className="h-5 w-5" />
                  System Health
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-500 rounded-lg">
                      <Database className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-white font-medium">Database</p>
                      <p className="text-green-400 text-sm">Connected</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-500 rounded-lg">
                      <Zap className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-white font-medium">API</p>
                      <p className="text-green-400 text-sm">Operational</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-500 rounded-lg">
                      <Activity className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-white font-medium">Performance</p>
                      <p className="text-green-400 text-sm">Excellent</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Analytics Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* User Growth Chart */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-blue-400" />
                    User Growth (Last 7 Days)
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={[
                        { day: 'Mon', users: 120 },
                        { day: 'Tue', users: 135 },
                        { day: 'Wed', users: 142 },
                        { day: 'Thu', users: 158 },
                        { day: 'Fri', users: 165 },
                        { day: 'Sat', users: 178 },
                        { day: 'Sun', users: 192 }
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="day" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                          labelStyle={{ color: '#e2e8f0' }}
                        />
                        <Line type="monotone" dataKey="users" stroke="#3b82f6" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Click Activity Chart */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Activity className="h-5 w-5 text-green-400" />
                    Click Activity (Last 7 Days)
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={[
                        { day: 'Mon', clicks: 450 },
                        { day: 'Tue', clicks: 520 },
                        { day: 'Wed', clicks: 480 },
                        { day: 'Thu', clicks: 630 },
                        { day: 'Fri', clicks: 710 },
                        { day: 'Sat', clicks: 590 },
                        { day: 'Sun', clicks: 680 }
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="day" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                          labelStyle={{ color: '#e2e8f0' }}
                        />
                        <Area type="monotone" dataKey="clicks" stroke="#10b981" fill="#10b98120" strokeWidth={2} />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Plan Distribution */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <PieChartIcon className="h-5 w-5 text-purple-400" />
                    Subscription Plans
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={[
                            { name: 'Free', value: 65, fill: '#64748b' },
                            { name: 'Pro', value: 25, fill: '#3b82f6' },
                            { name: 'Enterprise', value: 10, fill: '#8b5cf6' }
                          ]}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                          outerRadius={80}
                          dataKey="value"
                        >
                        </Pie>
                        <Tooltip
                          contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Top Campaigns */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-orange-400" />
                    Top Campaigns
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={[
                        { campaign: 'Summer Sale', clicks: 1250 },
                        { campaign: 'Product Launch', clicks: 980 },
                        { campaign: 'Newsletter', clicks: 750 },
                        { campaign: 'Social Media', clicks: 620 },
                        { campaign: 'Email Campaign', clicks: 450 }
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="campaign" stroke="#94a3b8" angle={-45} textAnchor="end" height={80} />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                          labelStyle={{ color: '#e2e8f0' }}
                        />
                        <Bar dataKey="clicks" fill="#f97316" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity Feed */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-white text-lg flex items-center gap-2">
                  <Clock className="h-5 w-5 text-cyan-400" />
                  Recent Activity
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { user: 'john_doe', action: 'Created new campaign "Summer 2025"', time: '2 minutes ago', icon: FolderKanban },
                    { user: 'jane_smith', action: 'Upgraded to Pro plan', time: '15 minutes ago', icon: Star },
                    { user: 'mike_wilson', action: 'Created 5 new tracking links', time: '1 hour ago', icon: Link2 },
                    { user: 'sarah_jones', action: 'Submitted support ticket #1234', time: '2 hours ago', icon: MessageSquare },
                    { user: 'admin', action: 'Approved 3 pending users', time: '3 hours ago', icon: UserCheck }
                  ].map((activity, index) => (
                    <div key={index} className="flex items-start gap-3 p-3 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition-colors">
                      <div className="p-2 bg-slate-600 rounded-lg">
                        <activity.icon className="h-4 w-4 text-slate-300" />
                      </div>
                      <div className="flex-1">
                        <p className="text-white text-sm">
                          <span className="font-medium text-blue-400">{activity.user}</span> {activity.action}
                        </p>
                        <p className="text-slate-400 text-xs mt-1">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

{/* Users Tab */}
          <TabsContent value="users" className="space-y-6">
            {/* User Management Metric Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <StatCard icon={Users} label="Total Users" value={dashboardStats.totalUsers} color="bg-blue-500" />
              <StatCard icon={UserCheck} label="Active Users" value={dashboardStats.activeUsers} color="bg-green-500" />
              <StatCard icon={Clock} label="Pending Users" value={dashboardStats.pendingUsers} color="bg-yellow-500" />
              <StatCard icon={UserX} label="Suspended Users" value={dashboardStats.suspendedUsers} color="bg-red-500" />
              <StatCard icon={Key} label="Admin Count" value={dashboardStats.adminCount} color="bg-purple-500" />
            </div>

            {/* Main Users Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">All System Users</CardTitle>
                <div className="flex items-center gap-2">
                  <Input
                    placeholder="Search users..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-[180px] bg-slate-900 border-slate-700 text-white"
                  />
                  <Button onClick={loadUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                    <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Date Joined</TableHead>
                        <TableHead>Subscription Plan</TableHead>
                        <TableHead>Last Login</TableHead>
                        <TableHead>Account Type</TableHead>
                        <TableHead>Payment Status</TableHead>
                        <TableHead>Login Method</TableHead>
                        <TableHead>Verification Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.dateJoined || 'N/A'}</TableCell>
                          <TableCell>{user.subscriptionPlan || 'Free'}</TableCell>
                          <TableCell>{user.lastLogin || 'N/A'}</TableCell>
                          <TableCell>
                            <Badge
                              className={`text-xs ${user.role === 'main_admin' ? 'bg-red-500' : user.role === 'admin' ? 'bg-purple-500' : 'bg-blue-500'}`}
                            >
                              {user.role}
                            </Badge>
                          </TableCell>
                          <TableCell>{user.paymentStatus || 'N/A'}</TableCell>
                          <TableCell>{user.loginMethod || 'Email/Pass'}</TableCell>
                          <TableCell>{user.verificationStatus || 'Unverified'}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                {isMainAdmin && (
                                  <DropdownMenuItem onClick={() => handleEditUser(user)} className="text-white hover:bg-slate-700/50">
                                    <Edit className="h-4 w-4 mr-2" /> Edit User
                                  </DropdownMenuItem>
                                )}
                                <DropdownMenuSeparator className="bg-slate-700" />
                                {isMainAdmin && (
                                  <DropdownMenuItem onClick={() => handleDeleteUser(user)} className="text-red-400 hover:bg-red-500/20">
                                    <Trash2 className="h-4 w-4 mr-2" /> Delete User
                                  </DropdownMenuItem>
                                )}
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Pending Users Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Pending Users (Verification/Payment)</CardTitle>
                <Button onClick={loadPendingUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Date Joined</TableHead>
                        <TableHead>Verification Status</TableHead>
                        <TableHead>Payment Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {pendingUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.dateJoined || 'N/A'}</TableCell>
                          <TableCell>{user.verificationStatus || 'Unverified'}</TableCell>
                          <TableCell>{user.paymentStatus || 'N/A'}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleApproveUser(user)} className="text-green-400 hover:bg-green-500/20">
                                  <UserCheck className="h-4 w-4 mr-2" /> Approve User
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleSuspendUser(user)} className="text-red-400 hover:bg-red-500/20">
                                  <UserX className="h-4 w-4 mr-2" /> Suspend User
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Suspended/Disabled Accounts Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Suspended / Disabled Accounts</CardTitle>
                <Button onClick={loadSuspendedUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Suspension Date</TableHead>
                        <TableHead>Reason</TableHead>
                        <TableHead>Account Type</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {suspendedUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.suspensionDate || 'N/A'}</TableCell>
                          <TableCell>{user.reason || 'N/A'}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleUnsuspendUser(user)} className="text-green-400 hover:bg-green-500/20">
                                  <Unlock className="h-4 w-4 mr-2" /> Unsuspend
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Activity Logs Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">User Activity Logs</CardTitle>
                <Button onClick={loadActivityLogs} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>Timestamp</TableHead>
                        <TableHead>User ID</TableHead>
                        <TableHead>Action</TableHead>
                        <TableHead>Resource ID</TableHead>
                        <TableHead>IP Address</TableHead>
                        <TableHead>Location</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {activityLogs.map((log) => (
                        <TableRow key={log.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{log.timestamp}</TableCell>
                          <TableCell>{log.userId}</TableCell>
                          <TableCell>{log.action}</TableCell>
                          <TableCell>{log.resourceId || 'N/A'}</TableCell>
                          <TableCell>{log.ipAddress || 'N/A'}</TableCell>
                          <TableCell>{log.location || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {<TabsContent value="users" className="space-y-6">
            {/* User Management Metric Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <StatCard icon={Users} label="Total Users" value={dashboardStats.totalUsers} color="bg-blue-500" />
              <StatCard icon={UserCheck} label="Active Users" value={dashboardStats.activeUsers} color="bg-green-500" />
              <StatCard icon={Clock} label="Pending Users" value={dashboardStats.pendingUsers} color="bg-yellow-500" />
              <StatCard icon={UserX} label="Suspended Users" value={dashboardStats.suspendedUsers} color="bg-red-500" />
              <StatCard icon={Key} label="Admin Count" value={dashboardStats.adminCount} color="bg-purple-500" />
            </div>

            {/* Main Users Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">All System Users</CardTitle>
                <div className="flex items-center gap-2">
                  <Input
                    placeholder="Search users..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-[180px] bg-slate-900 border-slate-700 text-white"
                  />
                  <Button onClick={loadUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                    <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Date Joined</TableHead>
                        <TableHead>Subscription Plan</TableHead>
                        <TableHead>Last Login</TableHead>
                        <TableHead>Account Type</TableHead>
                        <TableHead>Payment Status</TableHead>
                        <TableHead>Login Method</TableHead>
                        <TableHead>Verification Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.dateJoined || 'N/A'}</TableCell>
                          <TableCell>{user.subscriptionPlan || 'Free'}</TableCell>
                          <TableCell>{user.lastLogin || 'N/A'}</TableCell>
                          <TableCell>
                            <Badge
                              className={`text-xs ${user.role === 'main_admin' ? 'bg-red-500' : user.role === 'admin' ? 'bg-purple-500' : 'bg-blue-500'}`}
                            >
                              {user.role}
                            </Badge>
                          </TableCell>
                          <TableCell>{user.paymentStatus || 'N/A'}</TableCell>
                          <TableCell>{user.loginMethod || 'Email/Pass'}</TableCell>
                          <TableCell>{user.verificationStatus || 'Unverified'}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                {isMainAdmin && (
                                  <DropdownMenuItem onClick={() => handleEditUser(user)} className="text-white hover:bg-slate-700/50">
                                    <Edit className="h-4 w-4 mr-2" /> Edit User
                                  </DropdownMenuItem>
                                )}
                                <DropdownMenuSeparator className="bg-slate-700" />
                                {isMainAdmin && (
                                  <DropdownMenuItem onClick={() => handleDeleteUser(user)} className="text-red-400 hover:bg-red-500/20">
                                    <Trash2 className="h-4 w-4 mr-2" /> Delete User
                                  </DropdownMenuItem>
                                )}
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Pending Users Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Pending Users (Verification/Payment)</CardTitle>
                <Button onClick={loadPendingUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Date Joined</TableHead>
                        <TableHead>Verification Status</TableHead>
                        <TableHead>Payment Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {pendingUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.dateJoined || 'N/A'}</TableCell>
                          <TableCell>{user.verificationStatus || 'Unverified'}</TableCell>
                          <TableCell>{user.paymentStatus || 'N/A'}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleApproveUser(user)} className="text-green-400 hover:bg-green-500/20">
                                  <UserCheck className="h-4 w-4 mr-2" /> Approve User
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleSuspendUser(user)} className="text-red-400 hover:bg-red-500/20">
                                  <UserX className="h-4 w-4 mr-2" /> Suspend User
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Suspended/Disabled Accounts Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Suspended / Disabled Accounts</CardTitle>
                <Button onClick={loadSuspendedUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Suspension Date</TableHead>
                        <TableHead>Reason</TableHead>
                        <TableHead>Account Type</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {suspendedUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.suspensionDate || 'N/A'}</TableCell>
                          <TableCell>{user.reason || 'N/A'}</TableCell>
                          <TableCell>{user.role}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Activity Logs Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">User Activity Logs</CardTitle>
                <Button onClick={loadActivityLogs} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>Timestamp</TableHead>
                        <TableHead>User ID</TableHead>
                        <TableHead>Action</TableHead>
                        <TableHead>Resource ID</TableHead>
                        <TableHead>IP Address</TableHead>
                        <TableHead>Location</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {activityLogs.map((log) => (
                        <TableRow key={log.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{log.timestamp}</TableCell>
                          <TableCell>{log.userId}</TableCell>
                          <TableCell>{log.action}</TableCell>
                          <TableCell>{log.resourceId || 'N/A'}</TableCell>
                          <TableCell>{log.ipAddress || 'N/A'}</TableCell>
                          <TableCell>{log.location || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

          <TabsContent value="campaigns" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>          <h2 className="text-xl sm:text-2xl font-bold">Campaign Management</h2>
                <p className="text-slate-400 text-xs sm:text-sm">View and manage all campaigns</p>
              </div>
              <Button className="bg-green-600 hover:bg-green-700 w-full sm:w-auto text-xs sm:text-sm">
                <Plus className="h-4 w-4 mr-2" />
                Create Campaign
              </Button>
            </div>

            {/* Search and Filter */}
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  placeholder="Search campaigns..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="bg-slate-800 border-slate-700 text-white pl-10"
                />
              </div>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="bg-slate-800 border-slate-700 text-white w-full sm:w-48">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-700 border-slate-600">
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="paused">Paused</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Campaigns Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Name</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">Status</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Links</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">Clicks</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden lg:table-cell">Created</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 text-right">Expand</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredCampaigns.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={6} className="text-center py-8 text-slate-400 text-xs sm:text-sm">
                            {loading ? 'Loading campaigns...' : 'No campaigns found.'}
                          </TableCell>
                        </TableRow>
                      ) : (
                        filteredCampaigns.map((campaign) => (
                          <React.Fragment key={campaign.id}>
                            <TableRow className="border-slate-700 hover:bg-slate-700/50">
                              <TableCell className="text-white text-xs sm:text-sm font-medium px-4 py-3">
                                <div className="flex items-center gap-2">
                                  <FolderKanban className="h-4 w-4 text-slate-400" />
                                  {campaign.name}
                                </div>
                              </TableCell>
                              <TableCell className="px-4 py-3 hidden sm:table-cell">
                                {getStatusBadge(campaign.status || 'active')}
                              </TableCell>
                              <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3">
                                {campaign.link_count || 0}
                              </TableCell>
                              <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">
                                {campaign.click_count || 0}
                              </TableCell>
                              <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden lg:table-cell">
                                {campaign.created_at ? new Date(campaign.created_at).toLocaleDateString() : 'N/A'}
                              </TableCell>
                              <TableCell className="text-right px-4 py-3">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => toggleCampaignExpansion(campaign.id)}
                                  className="text-slate-400 hover:text-white"
                                >
                                  {expandedCampaignId === campaign.id ? (
                                    <ChevronUp className="h-4 w-4" />
                                  ) : (
                                    <ChevronDown className="h-4 w-4" />
                                  )}
                                </Button>
                              </TableCell>
                            </TableRow>
                            {expandedCampaignId === campaign.id && (
                              <TableRow className="bg-slate-900/50 border-slate-700">
                                <TableCell colSpan={6} className="p-0">
                                  <div className="p-4 sm:p-6 space-y-4">
                                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                                      <div>
                                        <p className="text-slate-400 text-xs">Description</p>
                                        <p className="text-white text-sm">{campaign.description || 'No description'}</p>
                                      </div>
                                      <div>
                                        <p className="text-slate-400 text-xs">Owner</p>
                                        <p className="text-white text-sm">{campaign.owner_username || 'Unknown'}</p>
                                      </div>
                                      <div>
                                        <p className="text-slate-400 text-xs">Links</p>
                                        <p className="text-white text-sm">{campaign.link_count || 0}</p>
                                      </div>
                                      <div>
                                        <p className="text-slate-400 text-xs">Total Clicks</p>
                                        <p className="text-white text-sm">{campaign.click_count || 0}</p>
                                      </div>
                                    </div>

                                    {campaign.links && campaign.links.length > 0 && (
                                      <div>
                                        <h5 className="text-white font-semibold text-sm mb-2">Associated Links</h5>
                                        <div className="bg-slate-800 rounded-lg p-3">
                                          <div className="overflow-x-auto">
                                            <Table className="text-xs">
                                              <TableHeader>
                                                <TableRow className="border-slate-600">
                                                  <TableHead className="text-slate-300 text-xs px-2 py-1">Code</TableHead>
                                                  <TableHead className="text-slate-300 text-xs px-2 py-1 hidden sm:table-cell">URL</TableHead>
                                                  <TableHead className="text-slate-300 text-xs px-2 py-1">Clicks</TableHead>
                                                  <TableHead className="text-slate-300 text-xs px-2 py-1 text-right">Actions</TableHead>
                                                </TableRow>
                                              </TableHeader>
                                              <TableBody>
                                                {campaign.links.slice(0, 5).map((link) => (
                                                  <TableRow key={link.id} className="border-slate-600 hover:bg-slate-700/50">
                                                    <TableCell className="text-white text-xs font-mono px-2 py-1">
                                                      {link.short_code}
                                                    </TableCell>
                                                    <TableCell className="text-slate-300 text-xs px-2 py-1 hidden sm:table-cell">
                                                      <div className="truncate max-w-[200px]" title={link.target_url}>
                                                        {link.target_url}
                                                      </div>
                                                    </TableCell>
                                                    <TableCell className="text-slate-300 text-xs px-2 py-1">
                                                      {link.clicks || 0}
                                                    </TableCell>
                                                    <TableCell className="text-right px-2 py-1">
                                                      <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white text-xs h-6 px-2">
                                                        <ExternalLink className="h-3 w-3" />
                                                      </Button>
                                                    </TableCell>
                                                  </TableRow>
                                                ))}
                                              </TableBody>
                                            </Table>
                                          </div>
                                          {campaign.links.length > 5 && (
                                            <div className="text-center mt-2">
                                              <Button variant="outline" size="sm" className="text-xs">
                                                View All {campaign.links.length} Links
                                              </Button>
                                            </div>
                                          )}
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                </TableCell>
                              </TableRow>
                            )}
                          </React.Fragment>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Security Tab */}
          <TabsContent value="security" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Security Threats</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Monitor and manage security incidents</p>
              </div>
              <Button onClick={loadSecurityThreats} variant="outline" size="sm" className="text-xs sm:text-sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>

            {/* Security Overview Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-red-500 rounded-lg">
                      <AlertTriangle className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Active Threats</p>
                      <p className="text-white text-xl font-bold">{securityThreats.filter(t => t.status === 'active').length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-yellow-500 rounded-lg">
                      <Shield className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Blocked IPs</p>
                      <p className="text-white text-xl font-bold">{securityThreats.filter(t => t.blocked).length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-500 rounded-lg">
                      <CheckCircle className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Resolved</p>
                      <p className="text-white text-xl font-bold">{securityThreats.filter(t => t.status === 'resolved').length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-500 rounded-lg">
                      <Activity className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Total Threats</p>
                      <p className="text-white text-xl font-bold">{securityThreats.length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Security Threats Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">IP Address</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">Threat Type</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Severity</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">Timestamp</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 text-right">Status</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {securityThreats.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={5} className="text-center py-8 text-slate-400 text-xs sm:text-sm">
                            {loading ? 'Loading security threats...' : 'No security threats detected.'}
                          </TableCell>
                        </TableRow>
                      ) : (
                        securityThreats.map((threat) => (
                          <TableRow key={threat.id} className="border-slate-700 hover:bg-slate-700/50">
                            <TableCell className="text-white text-xs sm:text-sm font-mono px-4 py-3">
                              {threat.ip_address}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">
                              {threat.threat_type}
                            </TableCell>
                            <TableCell className="px-4 py-3">
                              {getStatusBadge(threat.severity)}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">
                              {threat.timestamp ? new Date(threat.timestamp).toLocaleString() : 'N/A'}
                            </TableCell>
                            <TableCell className="text-right px-4 py-3">
                              {getStatusBadge(threat.status)}
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Subscriptions Tab */}
          <TabsContent value="subscriptions" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Subscriptions</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Manage user subscriptions and plans</p>
              </div>
              <Button onClick={loadSubscriptions} variant="outline" size="sm" className="text-xs sm:text-sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>

            {/* Subscription Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-500 rounded-lg">
                      <CreditCard className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Active Subscriptions</p>
                      <p className="text-white text-xl font-bold">
                        {subscriptions.filter(s => s.status === 'active').length}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-orange-500 rounded-lg">
                      <Clock className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Expired</p>
                      <p className="text-white text-xl font-bold">
                        {subscriptions.filter(s => s.status === 'expired').length}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-500 rounded-lg">
                      <DollarSign className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Total Revenue</p>
                      <p className="text-white text-xl font-bold">$0</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Subscriptions Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">User</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">Plan</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Status</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">Expires</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {subscriptions.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={5} className="text-center py-8 text-slate-400 text-xs sm:text-sm">
                            {loading ? 'Loading subscriptions...' : 'No subscriptions found.'}
                          </TableCell>
                        </TableRow>
                      ) : (
                        subscriptions.map((sub) => (
                          <TableRow key={sub.id} className="border-slate-700 hover:bg-slate-700/50">
                            <TableCell className="text-white text-xs sm:text-sm px-4 py-3">
                              {sub.user_name || sub.user_email}
                            </TableCell>
                            <TableCell className="px-4 py-3 hidden sm:table-cell">
                              {getStatusBadge(sub.plan_type)}
                            </TableCell>
                            <TableCell className="px-4 py-3">
                              {getStatusBadge(sub.status)}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">
                              {sub.expiry_date ? new Date(sub.expiry_date).toLocaleDateString() : 'N/A'}
                            </TableCell>
                            <TableCell className="text-right px-4 py-3">
                              <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white text-xs">
                                Manage
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Support Tab */}
          <TabsContent value="support" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Support Tickets</h2>
                <p className="text-slate-400 text-xs sm:text-sm">Manage customer support requests</p>
              </div>
              <Button onClick={loadSupportTickets} variant="outline" size="sm" className="text-xs sm:text-sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>

            {/* Support Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-yellow-500 rounded-lg">
                      <MessageSquare className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Open</p>
                      <p className="text-white text-xl font-bold">
                        {supportTickets.filter(t => t.status === 'open').length}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-500 rounded-lg">
                      <Clock className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">In Progress</p>
                      <p className="text-white text-xl font-bold">
                        {supportTickets.filter(t => t.status === 'in_progress').length}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-500 rounded-lg">
                      <CheckCircle className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Closed</p>
                      <p className="text-white text-xl font-bold">
                        {supportTickets.filter(t => t.status === 'closed').length}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-purple-500 rounded-lg">
                      <Star className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-slate-400 text-xs">Total</p>
                      <p className="text-white text-xl font-bold">{supportTickets.length}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Support Tickets Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Ticket ID</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">Subject</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Status</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">Priority</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {supportTickets.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={5} className="text-center py-8 text-slate-400 text-xs sm:text-sm">
                            {loading ? 'Loading support tickets...' : 'No support tickets found.'}
                          </TableCell>
                        </TableRow>
                      ) : (
                        supportTickets.map((ticket) => (
                          <TableRow key={ticket.id} className="border-slate-700 hover:bg-slate-700/50">
                            <TableCell className="text-white text-xs sm:text-sm font-mono px-4 py-3">
                              {ticket.ticket_number || ticket.id}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">
                              <div className="truncate max-w-[200px]" title={ticket.subject}>
                                {ticket.subject}
                              </div>
                            </TableCell>
                            <TableCell className="px-4 py-3">
                              {getStatusBadge(ticket.status)}
                            </TableCell>
                            <TableCell className="px-4 py-3 hidden md:table-cell">
                              {getStatusBadge(ticket.priority)}
                            </TableCell>
                            <TableCell className="text-right px-4 py-3">
                              <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white text-xs">
                                View
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Audit Tab */}
          <TabsContent value="audit" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-xl sm:text-2xl font-bold">Audit Logs</h2>
                <p className="text-slate-400 text-xs sm:text-sm">System activity and user actions</p>
              </div>
              <div className="flex gap-2 w-full sm:w-auto">
                <Button onClick={loadAuditLogs} variant="outline" size="sm" className="text-xs sm:text-sm flex-1 sm:flex-none">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh
                </Button>
                <Button onClick={exportAuditLogs} variant="outline" size="sm" className="text-xs sm:text-sm flex-1 sm:flex-none">
                  <Download className="h-4 w-4 mr-2" />
                  Export CSV
                </Button>
              </div>
            </div>

            {/* Audit Logs Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-slate-700">
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">ID</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">User ID</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3">Action</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">Target</TableHead>
                        <TableHead className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden lg:table-cell">Timestamp</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {auditLogs.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={5} className="text-center py-8 text-slate-400 text-xs sm:text-sm">
                            {loading ? 'Loading audit logs...' : 'No audit logs found.'}
                          </TableCell>
                        </TableRow>
                      ) : (
                        auditLogs.map((log) => (
                          <TableRow key={log.id} className="border-slate-700 hover:bg-slate-700/50">
                            <TableCell className="text-white text-xs sm:text-sm font-mono px-4 py-3">
                              {log.id}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden sm:table-cell">
                              {log.actor_id || log.user_id}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3">
                              <div className="truncate max-w-[200px]" title={log.action}>
                                {log.action}
                              </div>
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden md:table-cell">
                              {log.target_type ? `${log.target_type}:${log.target_id}` : 'N/A'}
                            </TableCell>
                            <TableCell className="text-slate-300 text-xs sm:text-sm px-4 py-3 hidden lg:table-cell">
                              {log.created_at ? new Date(log.created_at).toLocaleString() : 
                               log.timestamp ? new Date(log.timestamp).toLocaleString() : 'N/A'}
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Domain Management */}
              <div className="lg:col-span-2 space-y-6">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg sm:text-xl flex items-center gap-2">
                      <Globe className="h-5 w-5" />
                      Domain Management
                    </CardTitle>
                    <CardDescription className="text-slate-400 text-xs sm:text-sm">
                      Manage domains for link creation ({domains.length} domains configured)
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Dialog open={showCreateDomainDialog} onOpenChange={setShowCreateDomainDialog}>
                      <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700 w-full text-xs sm:text-sm">
                          <Plus className="h-4 w-4 mr-2" />
                          Add Domain
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="bg-slate-800 border-slate-700 w-[95vw] sm:w-full max-w-2xl">
                        <DialogHeader>
                          <DialogTitle className="text-white">Add New Domain</DialogTitle>
                          <DialogDescription className="text-slate-400 text-xs sm:text-sm">
                            Configure a new domain for link shortening services
                          </DialogDescription>
                        </DialogHeader>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                          <div className="sm:col-span-2">
                            <Label className="text-white text-sm">Domain</Label>
                            <Input
                              value={newDomain.domain}
                              onChange={(e) => setNewDomain({ ...newDomain, domain: e.target.value })}
                              placeholder="e.g., mylinks.short.gy"
                              className="bg-slate-700 border-slate-600 text-white mt-1"
                            />
                          </div>
                          <div>
                            <Label className="text-white text-sm">Domain Type</Label>
                            <Select
                              value={newDomain.domain_type}
                              onValueChange={(value) => setNewDomain({ ...newDomain, domain_type: value })}
                            >
                              <SelectTrigger className="bg-slate-700 border-slate-600 text-white mt-1">
                                <SelectValue />
                              </SelectTrigger>
                              <SelectContent className="bg-slate-700 border-slate-600">
                                <SelectItem value="custom">Custom</SelectItem>
                                <SelectItem value="shortio">Short.io</SelectItem>
                                <SelectItem value="vercel">Vercel</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                          <div className="flex items-center space-x-2 mt-6">
                            <Switch
                              id="domain_active"
                              checked={newDomain.is_active}
                              onCheckedChange={(checked) => setNewDomain({ ...newDomain, is_active: checked })}
                            />
                            <Label htmlFor="domain_active" className="text-white text-sm">Active Domain</Label>
                          </div>
                          <div className="sm:col-span-2">
                            <Label className="text-white text-sm">Description</Label>
                            <Textarea
                              value={newDomain.description}
                              onChange={(e) => setNewDomain({ ...newDomain, description: e.target.value })}
                              placeholder="Optional description for this domain"
                              className="bg-slate-700 border-slate-600 text-white mt-1"
                              rows={2}
                            />
                          </div>
                          <div>
                            <Label className="text-white text-sm">API Key (Optional)</Label>
                            <Input
                              type="password"
                              value={newDomain.api_key}
                              onChange={(e) => setNewDomain({ ...newDomain, api_key: e.target.value })}
                              placeholder="Domain service API key"
                              className="bg-slate-700 border-slate-600 text-white mt-1"
                            />
                          </div>
                          <div>
                            <Label className="text-white text-sm">API Secret (Optional)</Label>
                            <Input
                              type="password"
                              value={newDomain.api_secret}
                              onChange={(e) => setNewDomain({ ...newDomain, api_secret: e.target.value })}
                              placeholder="Domain service API secret"
                              className="bg-slate-700 border-slate-600 text-white mt-1"
                            />
                          </div>
                        </div>
                        <DialogFooter className="flex gap-2 flex-col sm:flex-row">
                          <Button 
                            onClick={createDomain} 
                            className="bg-blue-600 hover:bg-blue-700 flex-1 sm:flex-none text-xs sm:text-sm"
                            disabled={loading}
                          >
                            {loading ? 'Adding...' : 'Add Domain'}
                          </Button>
                          <Button
                            onClick={() => setShowCreateDomainDialog(false)}
                            variant="outline"
                            className="flex-1 sm:flex-none text-xs sm:text-sm"
                          >
                            Cancel
                          </Button>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>

                    <div className="overflow-x-auto">
                      <Table className="text-xs sm:text-sm">
                        <TableHeader>
                          <TableRow className="border-slate-700">
                            <TableHead className="text-slate-300 px-2 py-2">Domain</TableHead>
                            <TableHead className="text-slate-300 px-2 py-2 hidden sm:table-cell">Type</TableHead>
                            <TableHead className="text-slate-300 px-2 py-2">Status</TableHead>
                            <TableHead className="text-slate-300 px-2 py-2 text-right">Actions</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {domains.length === 0 ? (
                            <TableRow>
                              <TableCell colSpan={4} className="text-center py-4 text-slate-400 text-xs">
                                {loading ? 'Loading domains...' : 'No domains configured yet.'}
                              </TableCell>
                            </TableRow>
                          ) : (
                            domains.map((domain) => (
                              <TableRow key={domain.id} className="border-slate-700 hover:bg-slate-700/50">
                                <TableCell className="text-white font-mono text-xs px-2 py-2">
                                  <div className="flex items-center gap-2">
                                    <Globe className="h-3 w-3 text-slate-400" />
                                    {domain.domain}
                                  </div>
                                </TableCell>
                                <TableCell className="text-slate-300 text-xs px-2 py-2 hidden sm:table-cell">
                                  {domain.domain_type}
                                </TableCell>
                                <TableCell className="px-2 py-2">
                                  {getStatusBadge(domain.is_active ? 'active' : 'inactive')}
                                </TableCell>
                                <TableCell className="text-right px-2 py-2">
                                  <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                      <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white text-xs h-6 px-2">
                                        <MoreVertical className="h-3 w-3" />
                                      </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent className="bg-slate-800 border-slate-700" align="end">
                                      <DropdownMenuItem className="text-slate-300 hover:bg-slate-700">
                                        <Edit className="h-4 w-4 mr-2" />
                                        Edit
                                      </DropdownMenuItem>
                                      <DropdownMenuItem className="text-slate-300 hover:bg-slate-700">
                                        <Key className="h-4 w-4 mr-2" />
                                        Verify
                                      </DropdownMenuItem>
                                      <DropdownMenuSeparator className="bg-slate-700" />
                                      <DropdownMenuItem 
                                        className="text-red-400 hover:bg-red-500/20"
                                        onClick={() => deleteDomain(domain.id)}
                                      >
                                        <Trash2 className="h-4 w-4 mr-2" />
                                        Delete
                                      </DropdownMenuItem>
                                    </DropdownMenuContent>
                                  </DropdownMenu>
                                </TableCell>
                              </TableRow>
                            ))
                          )}
                        </TableBody>
                      </Table>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* System Settings */}
              <div className="space-y-4">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white text-base sm:text-lg flex items-center gap-2">
                      <Sliders className="h-5 w-5" />
                      System Settings
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <AlertDialog open={systemDeleteDialog} onOpenChange={setSystemDeleteDialog}>
                      <AlertDialogTrigger asChild>
                        <Button variant="destructive" className="w-full text-xs sm:text-sm">
                          <Trash2 className="h-4 w-4 mr-2" />
                          Delete All System Data
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent className="bg-slate-800 border-slate-700 w-[95vw] sm:w-full">
                        <AlertDialogHeader>
                          <AlertDialogTitle className="text-red-500">Delete All System Data</AlertDialogTitle>
                          <AlertDialogDescription className="text-slate-400 text-xs sm:text-sm">
                            This action will permanently delete all system data including users, links, 
                            campaigns, and tracking data. This action cannot be undone.
                            <br /><br />
                            Type <strong>"DELETE ALL DATA"</strong> to confirm:
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <div className="my-4">
                          <Input
                            value={confirmText}
                            onChange={(e) => setConfirmText(e.target.value)}
                            placeholder='Type "DELETE ALL DATA" to confirm'
                            className="bg-slate-700 border-slate-600 text-white text-xs sm:text-sm"
                          />
                        </div>
                        <AlertDialogFooter className="flex gap-2 flex-col sm:flex-row">
                          <AlertDialogAction
                            onClick={deleteAllSystemData}
                            className="bg-red-600 hover:bg-red-700 flex-1 sm:flex-none text-xs sm:text-sm"
                            disabled={loading || confirmText !== 'DELETE ALL DATA'}
                          >
                            {loading ? 'Deleting...' : 'Delete All Data'}
                          </AlertDialogAction>
                          <AlertDialogCancel
                            onClick={() => {
                              setSystemDeleteDialog(false);
                              setConfirmText('');
                            }}
                            className="flex-1 sm:flex-none text-xs sm:text-sm"
                          >
                            Cancel
                          </AlertDialogCancel>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </CardContent>
                </Card>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white text-base sm:text-lg flex items-center gap-2">
                      <Database className="h-5 w-5" />
                      Database Info
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3 text-xs sm:text-sm">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-slate-400">Total Users</p>
                        <p className="text-white font-semibold">{dashboardStats.totalUsers}</p>
                      </div>
                      <div>
                        <p className="text-slate-400">Total Links</p>
                        <p className="text-white font-semibold">{dashboardStats.totalLinks}</p>
                      </div>
                      <div>
                        <p className="text-slate-400">Total Clicks</p>
                        <p className="text-white font-semibold">{dashboardStats.totalClicks}</p>
                      </div>
                      <div>
                        <p className="text-slate-400">Campaigns</p>
                        <p className="text-white font-semibold">{dashboardStats.totalCampaigns}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Telegram Integration */}
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white text-base sm:text-lg flex items-center gap-2">
                      <Send className="h-5 w-5" />
                      Telegram Notifications
                    </CardTitle>
                    <CardDescription className="text-slate-400 text-xs sm:text-sm">
                      Configure Telegram for system alerts and notifications.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="telegram_bot_token" className="text-white text-sm">Bot Token</Label>
                      <Input
                        id="telegram_bot_token"
                        type="password"
                        value={telegramSettings.botToken}
                        onChange={(e) => setTelegramSettings({ ...telegramSettings, botToken: e.target.value })}
                        placeholder="Enter your Telegram Bot Token"
                        className="bg-slate-700 border-slate-600 text-white text-xs sm:text-sm"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="telegram_chat_id" className="text-white text-sm">Admin Chat ID</Label>
                      <Input
                        id="telegram_chat_id"
                        value={telegramSettings.chatId}
                        onChange={(e) => setTelegramSettings({ ...telegramSettings, chatId: e.target.value })}
                        placeholder="Enter your Admin Chat ID"
                        className="bg-slate-700 border-slate-600 text-white text-xs sm:text-sm"
                      />
                      <p className="text-slate-500 text-xs">
                        This is the chat ID where system notifications will be sent.
                      </p>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 text-xs sm:text-sm">Status:</span>
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${telegramSettings.status === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                        <span className={`text-xs ${telegramSettings.status === 'connected' ? 'text-green-400' : 'text-red-400'}`}>
                          {telegramSettings.status === 'connected' ? 'Connected' : 'Disconnected'}
                        </span>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button 
                        onClick={testTelegramConnection} 
                        className="bg-blue-600 hover:bg-blue-700 flex-1 text-xs sm:text-sm"
                        disabled={loading}
                      >
                        <Zap className="h-4 w-4 mr-2" />
                        Test Connection
                      </Button>
                      <Button 
                        onClick={saveTelegramSettings} 
                        className="bg-green-600 hover:bg-green-700 flex-1 text-xs sm:text-sm"
                        disabled={loading}
                      >
                        <Save className="h-4 w-4 mr-2" />
                        Save Settings
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white text-base sm:text-lg flex items-center gap-2">
                      <MonitorSpeaker className="h-5 w-5" />
                      System Status
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 text-xs sm:text-sm">API Status</span>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-green-400 text-xs">Online</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 text-xs sm:text-sm">Database</span>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-green-400 text-xs">Connected</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400 text-xs sm:text-sm">Security</span>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-green-400 text-xs">Protected</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Crypto Payments Tab - Main Admin Only */}
          {isMainAdmin && (
            <TabsContent value="crypto" className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">Crypto Payment Integration</h2>
                  <p className="text-slate-400">Manage cryptocurrency payment processing</p>
                </div>
              </div>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Payment Gateways</CardTitle>
                  <CardDescription>Configure cryptocurrency payment processors</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <Card className="bg-slate-900 border-slate-700">
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3 mb-3">
                          <DollarSign className="h-8 w-8 text-orange-500" />
                          <div>
                            <h3 className="font-semibold text-white">Bitcoin</h3>
                            <Badge className="bg-green-500 text-white text-xs">Active</Badge>
                          </div>
                        </div>
                        <div className="text-xs text-slate-400 space-y-1">
                          <p>Network: Mainnet</p>
                          <p>Confirmations: 3</p>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="bg-slate-900 border-slate-700">
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3 mb-3">
                          <DollarSign className="h-8 w-8 text-blue-500" />
                          <div>
                            <h3 className="font-semibold text-white">Ethereum</h3>
                            <Badge className="bg-green-500 text-white text-xs">Active</Badge>
                          </div>
                        </div>
                        <div className="text-xs text-slate-400 space-y-1">
                          <p>Network: Mainnet</p>
                          <p>Confirmations: 12</p>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="bg-slate-900 border-slate-700">
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3 mb-3">
                          <DollarSign className="h-8 w-8 text-green-500" />
                          <div>
                            <h3 className="font-semibold text-white">USDT</h3>
                            <Badge className="bg-yellow-500 text-white text-xs">Pending</Badge>
                          </div>
                        </div>
                        <div className="text-xs text-slate-400 space-y-1">
                          <p>Network: ERC-20</p>
                          <p>Confirmations: 12</p>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  <div className="mt-6">
                    <Button className="bg-blue-600 hover:bg-blue-700">
                      <Plus className="h-4 w-4 mr-2" />
                      Add Payment Gateway
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          )}

          {/* System Telegram Integration Tab - Main Admin Only */}
          {isMainAdmin && (
            <TabsContent value="telegram" className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">System Telegram Integration</h2>
                  <p className="text-slate-400">Configure system-wide Telegram bots for all users (Main Admin Only)</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white">Notification Bot</CardTitle>
                    <CardDescription>Send system alerts and notifications</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label className="text-slate-400">Bot Token</Label>
                      <Input
                        type="password"
                        placeholder="Enter bot token"
                        className="bg-slate-900 border-slate-700 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-slate-400">Chat ID</Label>
                      <Input
                        placeholder="Enter chat ID"
                        className="bg-slate-900 border-slate-700 text-white"
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-slate-400">Enable Bot</Label>
                      <Switch />
                    </div>
                    <Button className="w-full bg-blue-600 hover:bg-blue-700">
                      <Save className="h-4 w-4 mr-2" />
                      Save Configuration
                    </Button>
                  </CardContent>
                </Card>

                <Card className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <CardTitle className="text-white">Support Bot</CardTitle>
                    <CardDescription>Handle customer support inquiries</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label className="text-slate-400">Bot Token</Label>
                      <Input
                        type="password"
                        placeholder="Enter bot token"
                        className="bg-slate-900 border-slate-700 text-white"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-slate-400">Chat ID</Label>
                      <Input
                        placeholder="Enter chat ID"
                        className="bg-slate-900 border-slate-700 text-white"
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label className="text-slate-400">Enable Bot</Label>
                      <Switch />
                    </div>
                    <Button className="w-full bg-blue-600 hover:bg-blue-700">
                      <Save className="h-4 w-4 mr-2" />
                      Save Configuration
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          )}

          {/* Global Broadcaster Tab - Admin+ */}
          {isAdmin && (
            <TabsContent value="broadcaster" className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">Global Broadcaster</h2>
                  <p className="text-slate-400">Send system-wide messages to all users</p>
                </div>
              </div>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Broadcast Message</CardTitle>
                  <CardDescription>Create and send notifications to all active users</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-slate-400">Message Title <span className="text-red-400">*</span></Label>
                    <Input
                      placeholder="Enter message title"
                      className="bg-slate-900 border-slate-700 text-white"
                      value={broadcastForm.title}
                      onChange={(e) => setBroadcastForm({...broadcastForm, title: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-slate-400">Message Content <span className="text-red-400">*</span></Label>
                    <Textarea
                      placeholder="Enter your broadcast message..."
                      rows={6}
                      className="bg-slate-900 border-slate-700 text-white"
                      value={broadcastForm.message}
                      onChange={(e) => setBroadcastForm({...broadcastForm, message: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-slate-400">Message Type</Label>
                    <Select value={broadcastForm.type} onValueChange={(val) => setBroadcastForm({...broadcastForm, type: val})}>
                      <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        <SelectItem value="info">Information</SelectItem>
                        <SelectItem value="warning">Warning</SelectItem>
                        <SelectItem value="success">Success</SelectItem>
                        <SelectItem value="error">Error</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label className="text-slate-400">Priority</Label>
                    <Select value={broadcastForm.priority} onValueChange={(val) => setBroadcastForm({...broadcastForm, priority: val})}>
                      <SelectTrigger className="bg-slate-900 border-slate-700 text-white">
                        <SelectValue placeholder="Select priority" />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        <SelectItem value="low">Low</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="high">High</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <Button
                    className="w-full bg-blue-600 hover:bg-blue-700"
                    onClick={sendBroadcast}
                    disabled={loading || !broadcastForm.title || !broadcastForm.message}
                  >
                    <MonitorSpeaker className="h-4 w-4 mr-2" />
                    {loading ? 'Sending...' : 'Broadcast to All Users'}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>
          )}

          {/* Pending Users Tab - Admin+ */}
          {isAdmin && (
            <TabsContent value="pending" className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold">Pending Users</h2>
                  <p className="text-slate-400">Review and approve user registrations</p>
                </div>
              </div>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Awaiting Approval</CardTitle>
                  <CardDescription>Users pending admin approval</CardDescription>
                </CardHeader>
                <CardContent>
                  {pendingUsers.length === 0 ? (
                    <div className="text-center py-12">
                      <UserCheck className="h-12 w-12 text-slate-600 mx-auto mb-4" />
                      <p className="text-slate-400">No pending users at this time</p>
                    </div>
                  ) : (
                    <ScrollArea className="h-[500px]">
                      <Table>
                        <TableHeader>
                          <TableRow className="border-slate-700">
                            <TableHead className="text-slate-400">Username</TableHead>
                            <TableHead className="text-slate-400">Email</TableHead>
                            <TableHead className="text-slate-400">Role</TableHead>
                            <TableHead className="text-slate-400">Registered</TableHead>
                            <TableHead className="text-slate-400">Actions</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {pendingUsers.map((user) => (
                            <TableRow key={user.id} className="border-slate-700">
                              <TableCell className="text-white font-medium">{user.username}</TableCell>
                              <TableCell className="text-slate-300">{user.email}</TableCell>
                              <TableCell>{getStatusBadge(user.role)}</TableCell>
                              <TableCell className="text-slate-400 text-sm">
                                {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                              </TableCell>
                              <TableCell>
                                <div className="flex gap-2">
                                  <Button
                                    size="sm"
                                    className="bg-green-600 hover:bg-green-700"
                                    onClick={() => approvePendingUser(user.id)}
                                    disabled={loading}
                                  >
                                    <Check className="h-4 w-4 mr-1" />
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
        </Tabs>
      </div>

      {/* User Details Dialog */}
      <Dialog open={showUserDetailsDialog} onOpenChange={setShowUserDetailsDialog}>
        <DialogContent className="bg-slate-800 border-slate-700 w-[95vw] sm:w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-white">User Details</DialogTitle>
            <DialogDescription className="text-slate-400">
              Comprehensive user information and activity
            </DialogDescription>
          </DialogHeader>
          {selectedUser && (
            <div className="space-y-4">
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
                  <div className="mt-1">{getStatusBadge(selectedUser.role)}</div>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Status</Label>
                  <div className="mt-1">{getStatusBadge(selectedUser.status || 'active')}</div>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Plan Type</Label>
                  <div className="mt-1">{getStatusBadge(selectedUser.plan_type || 'free')}</div>
                </div>
                <div>
                  <Label className="text-slate-400 text-xs">Created</Label>
                  <p className="text-white">
                    {selectedUser.created_at ? new Date(selectedUser.created_at).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
              </div>
              
              <Separator className="bg-slate-700" />
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="flex items-center gap-2">
                  <Switch checked={selectedUser.is_active} disabled />
                  <Label className="text-slate-400 text-xs">Active Account</Label>
                </div>
                <div className="flex items-center gap-2">
                  <Switch checked={selectedUser.is_verified} disabled />
                  <Label className="text-slate-400 text-xs">Verified Email</Label>
                </div>
              </div>
              
              {selectedUser.subscription_expiry && (
                <div>
                  <Label className="text-slate-400 text-xs">Subscription Expires</Label>
                  <p className="text-white">
                    {new Date(selectedUser.subscription_expiry).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
          )}
          <DialogFooter>
            <Button 
              onClick={() => setShowUserDetailsDialog(false)}
              variant="outline"
              className="text-xs sm:text-sm"
            >
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
                                <DropdownMenuSeparator className="bg-slate-700" />
                                {isMainAdmin && (
                                  <DropdownMenuItem onClick={() => handleDeleteUser(user)} className="text-red-400 hover:bg-red-500/20">
                                    <Trash2 className="h-4 w-4 mr-2" /> Delete User
                                  </DropdownMenuItem>
                                )}
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Pending Users Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Pending Users (Verification/Payment)</CardTitle>
                <Button onClick={loadPendingUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Date Joined</TableHead>
                        <TableHead>Verification Status</TableHead>
                        <TableHead>Payment Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {pendingUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.dateJoined || 'N/A'}</TableCell>
                          <TableCell>{user.verificationStatus || 'Unverified'}</TableCell>
                          <TableCell>{user.paymentStatus || 'N/A'}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleApproveUser(user)} className="text-green-400 hover:bg-green-500/20">
                                  <UserCheck className="h-4 w-4 mr-2" /> Approve User
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleSuspendUser(user)} className="text-red-400 hover:bg-red-500/20">
                                  <UserX className="h-4 w-4 mr-2" /> Suspend User
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Suspended/Disabled Accounts Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">Suspended / Disabled Accounts</CardTitle>
                <Button onClick={loadSuspendedUsers} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>User ID</TableHead>
                        <TableHead>Username</TableHead>
                        <TableHead>Email</TableHead>
                        <TableHead>Suspension Date</TableHead>
                        <TableHead>Reason</TableHead>
                        <TableHead>Account Type</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {suspendedUsers.map((user) => (
                        <TableRow key={user.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{user.id}</TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell>{user.email || 'N/A'}</TableCell>
                          <TableCell>{user.suspensionDate || 'N/A'}</TableCell>
                          <TableCell>{user.reason || 'N/A'}</TableCell>
                          <TableCell>{user.role}</TableCell>
                          <TableCell className="text-right">
                            <DropdownMenu>
                              <DropdownMenuTrigger asChild>
                                <Button variant="ghost" className="h-8 w-8 p-0">
                                  <MoreVertical className="h-4 w-4" />
                                </Button>
                              </DropdownMenuTrigger>
                              <DropdownMenuContent align="end" className="bg-slate-900 border-slate-700">
                                <DropdownMenuItem onClick={() => handleViewUser(user)} className="text-white hover:bg-slate-700/50">
                                  <Eye className="h-4 w-4 mr-2" /> View Details
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => handleUnsuspendUser(user)} className="text-green-400 hover:bg-green-500/20">
                                  <Unlock className="h-4 w-4 mr-2" /> Unsuspend
                                </DropdownMenuItem>
                              </DropdownMenuContent>
                            </DropdownMenu>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>

            {/* Activity Logs Table */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-xl font-semibold">User Activity Logs</CardTitle>
                <Button onClick={loadActivityLogs} size="sm" variant="outline" className="text-xs bg-slate-900 border-slate-700 hover:bg-slate-700">
                  <RefreshCw className={`h-3 w-3 mr-1 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="text-xs text-slate-400">
                        <TableHead>Timestamp</TableHead>
                        <TableHead>User ID</TableHead>
                        <TableHead>Action</TableHead>
                        <TableHead>Resource ID</TableHead>
                        <TableHead>IP Address</TableHead>
                        <TableHead>Location</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {activityLogs.map((log) => (
                        <TableRow key={log.id} className="text-sm border-slate-700 hover:bg-slate-700/50">
                          <TableCell>{log.timestamp}</TableCell>
                          <TableCell>{log.userId}</TableCell>
                          <TableCell>{log.action}</TableCell>
                          <TableCell>{log.resourceId || 'N/A'}</TableCell>
                          <TableCell>{log.ipAddress || 'N/A'}</TableCell>
                          <TableCell>{log.location || 'N/A'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>




