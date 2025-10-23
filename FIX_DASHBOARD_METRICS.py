#!/usr/bin/env python3
"""
Fix Dashboard Metrics Design Consistency
Makes Dashboard metrics match the design of other tabs
"""

import re

def fix_dashboard_metrics():
    """Update Dashboard metrics to use consistent design"""
    
    with open('src/components/Dashboard.jsx', 'r') as f:
        content = f.read()
    
    # Define the pattern mapping
    replacements = [
        # Blue card
        ('border-l-4 border-l-blue-500 bg-gradient-to-br from-blue-50/50 to-transparent dark:from-blue-950/20',
         'bg-gradient-to-br from-blue-500/10 to-blue-600/5 border-blue-500/20'),
        
        # Green card
        ('border-l-4 border-l-green-500 bg-gradient-to-br from-green-50/50 to-transparent dark:from-green-950/20',
         'bg-gradient-to-br from-green-500/10 to-green-600/5 border-green-500/20'),
        
        # Purple card
        ('border-l-4 border-l-purple-500 bg-gradient-to-br from-purple-50/50 to-transparent dark:from-purple-950/20',
         'bg-gradient-to-br from-purple-500/10 to-purple-600/5 border-purple-500/20'),
        
        # Orange card
        ('border-l-4 border-l-orange-500 bg-gradient-to-br from-orange-50/50 to-transparent dark:from-orange-950/20',
         'bg-gradient-to-br from-orange-500/10 to-orange-600/5 border-orange-500/20'),
        
        # Emerald card
        ('border-l-4 border-l-emerald-500 bg-gradient-to-br from-emerald-50/50 to-transparent dark:from-emerald-950/20',
         'bg-gradient-to-br from-emerald-500/10 to-emerald-600/5 border-emerald-500/20'),
        
        # Yellow card
        ('border-l-4 border-l-yellow-500 bg-gradient-to-br from-yellow-50/50 to-transparent dark:from-yellow-950/20',
         'bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 border-yellow-500/20'),
        
        # Indigo card
        ('border-l-4 border-l-indigo-500 bg-gradient-to-br from-indigo-50/50 to-transparent dark:from-indigo-950/20',
         'bg-gradient-to-br from-indigo-500/10 to-indigo-600/5 border-indigo-500/20'),
        
        # Cyan card
        ('border-l-4 border-l-cyan-500 bg-gradient-to-br from-cyan-50/50 to-transparent dark:from-cyan-950/20',
         'bg-gradient-to-br from-cyan-500/10 to-cyan-600/5 border-cyan-500/20'),
        
        # Red card
        ('border-l-4 border-l-red-500 bg-gradient-to-br from-red-50/50 to-transparent dark:from-red-950/20',
         'bg-gradient-to-br from-red-500/10 to-red-600/5 border-red-500/20'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Also update the metrics structure to match other tabs
    # Replace compact p-3 padding with p-6 for consistency
    content = re.sub(
        r'<CardContent className="p-3">',
        '<CardContent className="p-6">',
        content
    )
    
    # Update text styling to match other tabs - slate colors
    content = re.sub(
        r'<p className="text-xs font-medium text-muted-foreground uppercase">',
        '<p className="text-sm font-medium text-slate-400 mb-1">',
        content
    )
    
    # Update number styling
    content = re.sub(
        r'<p className="text-2xl font-bold">',
        '<p className="text-3xl font-bold text-white">',
        content
    )
    
    with open('src/components/Dashboard.jsx', 'w') as f:
        f.write(content)
    
    print("✓ Dashboard metrics updated to match other tabs' design")

if __name__ == "__main__":
    fix_dashboard_metrics()
    print("\n✓ Dashboard design consistency fix applied!")
