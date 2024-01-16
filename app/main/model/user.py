from .. import db
from enum import Enum
import uuid
import datetime
from ..util.helper import convert_to_local_time, is_valid_email, create_token
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(Enum):
    admin = "admin"
    user = "user"


class UserStatus(Enum):
    active = "active"
    inactive = "inactive"


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.user)
    status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.active)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "username": self.username,
            "email": self.email,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
            "role": self.role.value,
            "status": self.status.value,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all_users(self, page):
        try:
            limit = 50
            if page is not None:
                offset = (page - 1) * limit
                users = self.query.limit(limit).offset(offset).all()
            else:
                users = self.query.all()
            return [user.serialize() for user in users]
        except Exception as e:
            raise e

    def register_user(self, data):
        try:
            password = generate_password_hash(data.get("password"))
            email = data.get("email")
            if not is_valid_email(email):
                raise Exception("The email is invalid")
            user = self.query.filter_by(email=email).first()
            if user:
                raise Exception("This email has already registered")

            self.public_id = str(uuid.uuid4())
            self.username = data.get("username")
            self.email = email
            self.password = password
            self.role = data.get("role")
            self.status = data.get("status")
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()
            self.save()
            return self.serialize()
        except Exception as e:
            raise e

    def get_user_by_id(self, public_id, user_id):
        try:
            user = self.query.filter_by(public_id=public_id).first()
            if not user:
                raise Exception("User not found. Invalid ID")
            authorized_user = self.check_user_authorization(public_id, user_id)
            if authorized_user:
                return user.serialize()
        except Exception as e:
            raise e

    def delete_user(self, public_id, user_id):
        try:
            user = self.query.filter_by(public_id=public_id).first()
            if not user:
                raise Exception("User not found. Please enter a valid id")
            authorized_user = self.check_user_authorization(public_id, user_id)
            if authorized_user:
                # user.deleted_at = datetime.datetime.utcnow() soft delete
                db.session.delete(user)
                db.session.commit()
                return True
        except Exception as e:
            raise e

    def update_user(self, public_id, data, user_id):
        try:
            user = self.query.filter_by(public_id=public_id).first()
            if not user:
                raise Exception("User not found. Invalid ID")
            authorized_user = self.check_user_authorization(public_id, user_id)
            if authorized_user:
                password = generate_password_hash(data.get("password"))
                email = data.get("email")
                if not is_valid_email(email):
                    raise Exception("The email is invalid")
                user.username = data.get("username")
                user.email = email
                user.password = password
                user.updated_at = datetime.datetime.utcnow()
                db.session.commit()
                return user.serialize()
        except Exception as e:
            raise e

    def update_user_status(self, public_id, data):
        try:
            user = self.query.filter_by(public_id=public_id).first()
            if not user:
                raise Exception("User not found. Invalid ID")
            else:
                isBanned = data.get("banned")
                if isBanned:
                    status = "inactive"
                else:
                    status = "active"
                user.status = status
                user.updated_at = datetime.datetime.utcnow()
                db.session.commit()
                return user.serialize()
        except Exception as e:
            raise e

    # please never return this
    def serialize_entire_data(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,
            "status": self.status.value,
        }

    def user_auth(self, data):
        try:
            user = self.query.filter_by(email=data.get("email")).first()
            if not user:
                raise Exception("User not found. Invalid ID")

            user_data = user.serialize_entire_data()
            if check_password_hash(user_data["password"], data.get("password")):
                return create_token(user_data)
            else:
                raise Exception("Incorrect password. Please try again")

        except Exception as e:
            raise e

    def check_user_authorization(self, public_id, user_id):
        try:
            user = self.query.filter_by(public_id=public_id).first()
            check_user = user.serialize_entire_data()
            if check_user["id"] != user_id:
                raise Exception("Access denied")
            else:
                return True
        except Exception as e:
            raise e
