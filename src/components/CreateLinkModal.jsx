'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Plus,
  Eye,
  EyeOff,
  Copy,
  RefreshCw,
  Globe,
  Lock,
  Zap,
  AlertCircle,
  CheckCircle,
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function CreateLinkModal({ onLinkCreated, campaigns = [] }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [domains, setDomains] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [formData, setFormData] = useState({
    originalUrl: '',
    customCode: '',
    password: '',
    domain: '',
    campaignId: '',
    expiryDate: '',
    maxClicks: '',
    description: '',
  });

  useEffect(() => {
    if (open) {
      loadDomains();
    }
  }, [open]);

  const loadDomains = async () => {
    try {
      const response = await fetch('/api/admin/domains', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      if (response.ok) {
        const data = await response.json();
        setDomains(data.domains || []);
        if (data.domains && data.domains.length > 0) {
          setFormData(prev => ({
            ...prev,
            domain: data.domains[0].id
          }));
        }
      }
    } catch (error) {
      console.error('Failed to load domains:', error);
    }
  };

  const generateCustomCode = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
      code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setFormData(prev => ({
      ...prev,
      customCode: code
    }));
  };

  const regenerateTrackingLink = () => {
    generateCustomCode();
    setSuccess('Tracking link regenerated');
    setTimeout(() => setSuccess(null), 2000);
  };

  const validateForm = () => {
    if (!formData.originalUrl) {
      setError('Please enter a destination URL');
      return false;
    }
    if (!formData.domain) {
      setError('Please select a domain');
      return false;
    }
    try {
      new URL(formData.originalUrl);
    } catch {
      setError('Please enter a valid URL');
      return false;
    }
    return true;
  };

  const createLink = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/links/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          original_url: formData.originalUrl,
          custom_code: formData.customCode || undefined,
          password: formData.password || undefined,
          domain_id: formData.domain,
          campaign_id: formData.campaignId || undefined,
          expiry_date: formData.expiryDate || undefined,
          max_clicks: formData.maxClicks ? parseInt(formData.maxClicks) : undefined,
          description: formData.description || undefined,
        })
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess('Link created successfully!');
        setFormData({
          originalUrl: '',
          customCode: '',
          password: '',
          domain: domains.length > 0 ? domains[0].id : '',
          campaignId: '',
          expiryDate: '',
          maxClicks: '',
          description: '',
        });
        setTimeout(() => {
          setOpen(false);
          setSuccess(null);
          if (onLinkCreated) onLinkCreated(data);
        }, 1500);
      } else {
        const data = await response.json();
        setError(data.error || 'Failed to create link');
      }
    } catch (error) {
      setError('Error creating link: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const selectedDomain = domains.find(d => d.id === formData.domain);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="bg-green-600 hover:bg-green-700 text-white text-xs sm:text-sm">
          <Plus className="h-4 w-4 mr-2" />
          Create New Link
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-slate-800 border-slate-700 w-[95vw] sm:w-full max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-white text-lg sm:text-xl">Create New Tracking Link</DialogTitle>
          <DialogDescription className="text-slate-400 text-xs sm:text-sm">
            Create a new shortened link with advanced tracking and protection options
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {error && (
            <div className="p-3 sm:p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-200 text-xs sm:text-sm flex items-start gap-2">
              <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
              <div>
                {error}
                <button onClick={() => setError(null)} className="ml-2 text-red-100 hover:text-red-50">✕</button>
              </div>
            </div>
          )}

          {success && (
            <div className="p-3 sm:p-4 bg-green-500/20 border border-green-500 rounded-lg text-green-200 text-xs sm:text-sm flex items-start gap-2">
              <CheckCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
              <div>{success}</div>
            </div>
          )}

          {/* Destination URL */}
          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Destination URL *</label>
            <Input
              type="url"
              placeholder="https://example.com/page"
              value={formData.originalUrl}
              onChange={(e) => setFormData(prev => ({ ...prev, originalUrl: e.target.value }))}
              className="bg-slate-700 border-slate-600 text-white text-xs sm:text-sm"
            />
            <p className="text-slate-400 text-xs">The URL where users will be redirected after clicking your link</p>
          </div>

          {/* Domain Selection */}
          <div className="space-y-2">
            <label className="text-white text-sm font-medium flex items-center gap-2">
              <Globe className="h-4 w-4" />
              Select Domain *
            </label>
            {domains.length === 0 ? (
              <div className="p-3 sm:p-4 bg-yellow-500/20 border border-yellow-500 rounded-lg text-yellow-200 text-xs sm:text-sm">
                No domains available. Please contact your administrator to add domains.
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {domains.map(domain => (
                  <button
                    key={domain.id}
                    onClick={() => setFormData(prev => ({ ...prev, domain: domain.id }))}
                    className={`p-3 rounded-lg border text-left text-xs sm:text-sm transition ${
                      formData.domain === domain.id
                        ? 'bg-blue-600 border-blue-500 text-white'
                        : 'bg-slate-700 border-slate-600 text-slate-300 hover:border-slate-500'
                    }`}
                  >
                    <div className="font-mono">{domain.domain}</div>
                    <div className="text-xs opacity-75 mt-1">{domain.status}</div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Generated Link Preview */}
          {selectedDomain && (
            <Card className="bg-slate-700 border-slate-600">
              <CardHeader className="pb-3">
                <CardTitle className="text-white text-sm">Generated Link</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="bg-slate-800 p-3 rounded-lg flex items-center justify-between gap-2">
                  <code className="text-blue-400 text-xs sm:text-sm break-all">
                    {selectedDomain.domain}/{formData.customCode || 'XXXXXX'}
                  </code>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-slate-400 hover:text-white flex-shrink-0"
                    onClick={() => {
                      navigator.clipboard.writeText(`${selectedDomain.domain}/${formData.customCode || 'XXXXXX'}`);
                      setSuccess('Link copied to clipboard');
                      setTimeout(() => setSuccess(null), 2000);
                    }}
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Custom Code & Regenerate */}
          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Custom Code</label>
            <div className="flex gap-2">
              <Input
                placeholder="Leave empty for auto-generated"
                value={formData.customCode}
                onChange={(e) => setFormData(prev => ({ ...prev, customCode: e.target.value }))}
                className="bg-slate-700 border-slate-600 text-white text-xs sm:text-sm flex-1"
              />
              <Button
                onClick={regenerateTrackingLink}
                variant="outline"
                size="sm"
                className="text-xs sm:text-sm flex-shrink-0"
              >
                <RefreshCw className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-slate-400 text-xs">Create a memorable short code or let us generate one</p>
          </div>

          {/* Password Protection */}
          <div className="space-y-2">
            <label className="text-white text-sm font-medium flex items-center gap-2">
              <Lock className="h-4 w-4" />
              Password Protection
            </label>
            <div className="relative">
              <Input
                type={showPassword ? 'text' : 'password'}
                placeholder="Optional password for link access"
                value={formData.password}
                onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                className="bg-slate-700 border-slate-600 text-white text-xs sm:text-sm pr-10"
              />
              <button
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            <p className="text-slate-400 text-xs">Protect your link with a password</p>
          </div>

          {/* Campaign Selection */}
          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Campaign</label>
            <select
              value={formData.campaignId}
              onChange={(e) => setFormData(prev => ({ ...prev, campaignId: e.target.value }))}
              className="w-full bg-slate-700 border border-slate-600 text-white rounded-md p-2 text-xs sm:text-sm"
            >
              <option value="">Select a campaign (optional)</option>
              {campaigns.map(campaign => (
                <option key={campaign.id} value={campaign.id}>
                  {campaign.name}
                </option>
              ))}
            </select>
          </div>

          {/* Advanced Options */}
          <div className="space-y-4 p-4 bg-slate-700/50 rounded-lg">
            <h4 className="text-white text-sm font-medium flex items-center gap-2">
              <Zap className="h-4 w-4" />
              Advanced Options
            </h4>

            <div className="space-y-2">
              <label className="text-white text-xs sm:text-sm">Expiry Date</label>
              <Input
                type="datetime-local"
                value={formData.expiryDate}
                onChange={(e) => setFormData(prev => ({ ...prev, expiryDate: e.target.value }))}
                className="bg-slate-600 border-slate-500 text-white text-xs sm:text-sm"
              />
            </div>

            <div className="space-y-2">
              <label className="text-white text-xs sm:text-sm">Max Clicks</label>
              <Input
                type="number"
                placeholder="Unlimited if empty"
                value={formData.maxClicks}
                onChange={(e) => setFormData(prev => ({ ...prev, maxClicks: e.target.value }))}
                className="bg-slate-600 border-slate-500 text-white text-xs sm:text-sm"
              />
            </div>

            <div className="space-y-2">
              <label className="text-white text-xs sm:text-sm">Description</label>
              <textarea
                placeholder="Add notes about this link"
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                className="w-full bg-slate-600 border border-slate-500 text-white rounded-md p-2 text-xs sm:text-sm"
                rows="2"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2 flex-col sm:flex-row">
            <Button
              onClick={createLink}
              disabled={loading}
              className="bg-green-600 hover:bg-green-700 flex-1 text-xs sm:text-sm"
            >
              {loading ? 'Creating...' : 'Create Link'}
            </Button>
            <Button
              onClick={() => setOpen(false)}
              variant="outline"
              className="flex-1 text-xs sm:text-sm"
            >
              Cancel
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

