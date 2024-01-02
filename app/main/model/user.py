from .. import db
from enum import Enum
import uuid
import datetime
from ..util.helper import convert_to_local_time
from werkzeug.security import generate_password_hash, check_password_hash


class UserRole(Enum):
    admin = 'admin'
    user = 'user'

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.user)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def serialize(self):
        print("serialize")
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "username": self.username,
            "email": self.email,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
            "role":self.role.value,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all_users(self):
        users = self.query.all()
        return [user.serialize() for user in users]
    
    def register_user(self, data):
        try:
            hashed_password = generate_password_hash(data.get("password"))

            self.public_id = str(uuid.uuid4())
            self.username = data.get("username")
            self.email = data.get("email")
            self.password = hashed_password
            self.role = data.get("role")
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()

            self.save()
            return self.serialize()

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
