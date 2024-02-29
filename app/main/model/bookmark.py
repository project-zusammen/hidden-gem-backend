from .. import db
import uuid
import datetime
from ..util.helper import convert_to_local_time
from .review import Review
from .user import User

review_instance = Review()
user_instance = User()


class Bookmark(db.Model):
    __tablename__ = "bookmark"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return f"<Bookmark(user_id={self.user_id}, review_id={self.review_id})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        user_public_id = user_instance.get_user_public_id_by_id(self.user_id)
        review_model = Review()
        review_public_id = review_model.get_review_public_id(self.review_id)
        return {
            "public_id": self.public_id,
            "user_id": user_public_id,
            "review_id": review_public_id,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_bookmark(self, data, user_id):
        try:
            review_id = review_instance.get_review_id_by_public_id(
                data.get("review_id")
            )
            bookmark = Bookmark(
                public_id = str(uuid.uuid4()),
                user_id = user_id,
                review_id = review_id,
                created_at = datetime.datetime.utcnow(),
                updated_at = datetime.datetime.utcnow(),
            )

            bookmark.save()
            return bookmark.serialize()
        except Exception as e:
            raise e

    def get_bookmark_by_userid(self, user_id):
        try:
            results = self.query.filter_by(user_id=user_id)
            bookmarks = [data.serialize() for data in results]
            return bookmarks
        except Exception as e:
            raise e

    def delete_bookmark(self, bookmark_id, user_id):
        try:
            bookmark = self.query.filter_by(public_id=bookmark_id).first()
            if not bookmark:
                raise Exception("Bookmark not found. Invalid ID")
            id = bookmark.user_id
            if user_id != id:
                raise Exception("Access denied")

            db.session.delete(bookmark)
            db.session.commit()
            return True
        except Exception as e:
            raise e
