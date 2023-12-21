from app.main import create_app, db
import pymysql
pymysql.install_as_MySQLdb()

# Create the Flask app
app = create_app()

# Use app context to run operations
with app.app_context():
    # Create all tables
    db.create_all()

print("Database tables created successfully.")
