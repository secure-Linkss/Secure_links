from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_7CcKbPRm2GDw@ep-odd-thunder-ade4ip4a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)

    db.init_app(app)

    from .routes.auth import auth_bp
    from .routes.links import links_bp
    from .routes.track import track_bp
    from .routes.analytics import analytics_bp
    from .routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(links_bp)
    app.register_blueprint(track_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(settings_bp)

    return app

