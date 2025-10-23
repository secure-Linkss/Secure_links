/**
 * Session Tracking Script for Brain Link Tracker
 * This script should be embedded on landing pages to track session duration and page views
 */

(function() {
    // Configuration
    const HEARTBEAT_INTERVAL = 30000; // 30 seconds
    const API_BASE_URL = window.location.origin;
    
    // Session tracking variables
    let sessionStartTime = Date.now();
    let currentDuration = 0;
    let pageViews = 1;
    let heartbeatInterval;
    let uniqueId = null;
    let linkId = null;
    
    // Extract tracking parameters from URL
    function getTrackingParams() {
        const urlParams = new URLSearchParams(window.location.search);
        uniqueId = urlParams.get('uid') || localStorage.getItem('bt_unique_id');
        linkId = urlParams.get('link_id') || localStorage.getItem('bt_link_id');
        
        // Store in localStorage for persistence
        if (uniqueId) localStorage.setItem('bt_unique_id', uniqueId);
        if (linkId) localStorage.setItem('bt_link_id', linkId);
    }
    
    // Calculate current session duration
    function getCurrentDuration() {
        return Math.floor((Date.now() - sessionStartTime) / 1000);
    }
    
    // Send heartbeat to server
    function sendHeartbeat() {
        currentDuration = getCurrentDuration();
        
        if (!uniqueId && !linkId) return;
        
        const data = {
            unique_id: uniqueId,
            link_id: linkId,
            duration: currentDuration
        };
        
        fetch(`${API_BASE_URL}/track/heartbeat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).catch(err => console.log('Heartbeat failed:', err));
    }
    
    // Update session duration on server
    function updateSessionDuration() {
        currentDuration = getCurrentDuration();
        
        if (!uniqueId && !linkId) return;
        
        const data = {
            unique_id: uniqueId,
            link_id: linkId,
            duration: currentDuration,
            page_views: pageViews
        };
        
        fetch(`${API_BASE_URL}/track/session-duration`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).catch(err => console.log('Session update failed:', err));
    }
    
    // Track page landed event
    function trackPageLanded() {
        if (!uniqueId && !linkId) return;
        
        const data = {
            unique_id: uniqueId,
            link_id: linkId
        };
        
        fetch(`${API_BASE_URL}/track/page-landed`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).catch(err => console.log('Page landed tracking failed:', err));
    }
    
    // Initialize tracking
    function initTracking() {
        getTrackingParams();
        
        if (!uniqueId && !linkId) {
            console.log('No tracking parameters found');
            return;
        }
        
        // Track that user landed on page
        trackPageLanded();
        
        // Start heartbeat
        heartbeatInterval = setInterval(sendHeartbeat, HEARTBEAT_INTERVAL);
        
        // Track page visibility changes
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                updateSessionDuration();
                clearInterval(heartbeatInterval);
            } else {
                sessionStartTime = Date.now() - (currentDuration * 1000);
                heartbeatInterval = setInterval(sendHeartbeat, HEARTBEAT_INTERVAL);
            }
        });
        
        // Track page unload
        window.addEventListener('beforeunload', function() {
            updateSessionDuration();
        });
        
        // Track page views (for SPAs)
        let currentUrl = window.location.href;
        setInterval(function() {
            if (window.location.href !== currentUrl) {
                currentUrl = window.location.href;
                pageViews++;
                updateSessionDuration();
            }
        }, 1000);
    }
    
    // Start tracking when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTracking);
    } else {
        initTracking();
    }
})();
