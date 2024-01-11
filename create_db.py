# Run this archive to create your local database
from pinterest_clone import app, database
from pinterest_clone.models import User, Post

with app.app_context():
    database.create_all()
