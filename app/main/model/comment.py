import uuid
from .. import db

class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    visible = db.Column(db.Boolean, nullable=False, default=True)


    def __init__(self, public_id, review_id, content, created_at, updated_at, upvotes=0, downvotes=0, visible=True):
        self.public_id = public_id
        # self.user_id = user_id
        self.review_id = review_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.visible = visible
    

    def __repr__(self):
        return f"<Comment(content={self.content})>"
    

    def serialize(self):
        return {
            'public_id': self.public_id,
            # 'user_id': self.user_id,
            'review_id': self.review_id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'visible': self.visible
        }
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
