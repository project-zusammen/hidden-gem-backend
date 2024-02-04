import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # comment_id = db.Column(db.Integer, db.ForeignKey('comment.id')) -> yang bener
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    visible = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Comment(content={self.content})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            # 'user_id': self.user_id,
            # 'comment_id': self.comment_id,
            "content": self.content,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "visible": self.visible,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_comment(self, data):
        try:
            self.public_id = str(uuid.uuid4())
            self.content = data.get("content")
        try:
            self.public_id = str(uuid.uuid4())
            self.content = data.get("content")

            if not self.content:
                raise Exception("Comment content is required")
            if not self.content:
                raise Exception("Comment content is required")

            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()
            self.upvotes = 0
            self.downvotes = 0
            self.visible = True
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()
            self.upvotes = 0
            self.downvotes = 0
            self.visible = True

            self.save()
            return self.serialize()
        except Exception as e:
            raise e

    def get_all_comments(self):
        try:
            comments = self.query.filter_by(visible=True).all()
            return [comment.serialize() for comment in comments]
        except Exception as e:
            raise e
            self.save()
            return self.serialize()
        except Exception as e:
            raise e

    def get_all_comments(self):
        try:
            comments = self.query.filter_by(visible=True).all()
            return [comment.serialize() for comment in comments]
        except Exception as e:
            raise e

    def get_comment_by_id(self, public_id):
        comment = self.query.filter_by(public_id=public_id, visible=True).first()
        try:
            return comment.serialize()
        except Exception as e:
            raise e
        comment = self.query.filter_by(public_id=public_id, visible=True).first()
        try:
            return comment.serialize()
        except Exception as e:
            raise e

    def delete_comment(self, public_id):
        try:
            comment = self.query.filter_by(public_id=public_id, visible=True).first()
            if not comment:
                return None
            else:
                comment.visible = False
                comment.updated_at = datetime.datetime.utcnow()
                comment.save()
                return comment.serialize()
        except Exception as e:
            raise e
        try:
            comment = self.query.filter_by(public_id=public_id, visible=True).first()
            if not comment:
                return None
            else:
                comment.visible = False
                comment.updated_at = datetime.datetime.utcnow()
                comment.save()
                return comment.serialize()
        except Exception as e:
            raise e

    def update_comment(self, public_id, data):
        try:
            comment = self.query.filter_by(public_id=public_id, visible=True).first()
            if not comment:
                return None
            else:
                comment.content = data.get("content")
                comment.updated_at = datetime.datetime.utcnow()
                comment.save()
                return comment.serialize()
        except Exception as e:
            raise e
        try:
            comment = self.query.filter_by(public_id=public_id, visible=True).first()
            if not comment:
                return None
            else:
                comment.content = data.get("content")
                comment.updated_at = datetime.datetime.utcnow()
                comment.save()
                return comment.serialize()
        except Exception as e:
            raise e

    def upvote_comment(self, public_id, upvote=True):
        try:
<<<<<<< HEAD
            # comment = self.get_comment_by_id(public_id)
=======
>>>>>>> main
            comment = self.query.filter_by(public_id=public_id, visible=True).first()
            if upvote:
                comment.upvotes += 1
            else:
                comment.downvotes += 1
            comment.updated_at = datetime.datetime.utcnow()
            comment.save()
            return comment.serialize()
        except Exception as e:
            raise e

    def update_visibility(self, public_id, visible=True):
        try:
            comment = self.query.filter_by(public_id=public_id).first()
            if not comment:
                return None
            else:
                comment.visible = visible
                comment.updated_at = datetime.datetime.utcnow()
                comment.save()
                return comment.serialize()
        except Exception as e:
            raise e
        try:
            comment = self.query.filter_by(public_id=public_id).first()
            if not comment:
                return None
            else:
                comment.visible = visible
                comment.updated_at = datetime.datetime.utcnow()
                comment.save()
                return comment.serialize()
        except Exception as e:
            raise e
