from src import create_app, db
from src.models.link import Link
from src.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username="Brain").first()
    if user:
        active_links = Link.query.filter_by(user_id=user.id, status="active").all()
        print(len(active_links))
    else:
        print("User \'Brain\' not found.")

