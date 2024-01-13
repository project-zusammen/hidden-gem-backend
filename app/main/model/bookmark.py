from .. import db
from enum import Enum
import uuid
import datetime
from ..util.helper import convert_to_local_time, is_valid_email, hash_password

class Bookmark(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
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
            "user_id": self.user_id,
            "review_id": self.review_id,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def create_bookmark(self, data):
        try:
            self.public_id = str(uuid.uuid4())
            self.user_id = data.get("user_id")
            self.review_id = data.get("review_id")
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()

            self.save()
            return self.serialize()

        except Exception as e:
            raise e
        
    def get_bookmark_by_userid(self, user_id):
        try:
            bookmark = self.query.filter_by(user_id=user_id)
            if not bookmark:
                raise Exception("The bookmark is empty")
            else:
                return bookmark.serialize()
        except Exception as e:
            raise e
        
    def delete_bookmark(self, public_id):
        try:
            bookmark = self.query.filter_by(public_id=public_id).first()
            if not bookmark:
                raise Exception("bookmark not found. Invalid ID")
            
            db.session.delete(bookmark)  
            db.session.commit()
            return True
        except Exception as e:
            raise e
    
    