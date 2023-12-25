import uuid
from .. import db
import datetime

class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    visible = db.Column(db.Boolean, nullable=False, default=True)


    # def __init__(self, public_id, title, content, location, created_at, updated_at, upvotes=0, downvotes=0, visible=True):
    #     self.public_id = public_id
    #     # self.user_id = user_id
    #     # self.category_id = category_id
    #     # self.region_id = region_id
    #     self.title = title
    #     self.content = content
    #     self.location = location
    #     self.created_at = created_at
    #     self.updated_at = updated_at
    #     self.upvotes = upvotes
    #     self.downvotes = downvotes
    #     self.visible = visible
    

    def __repr__(self):
        return f"<Review(title={self.title}, content={self.content})>"
    

    def serialize(self):
        return {
            'public_id': self.public_id,
            # 'user_id': self.user_id,
            # 'category_id': self.category_id,
            # 'region_id': self.region_id,
            'title': self.title,
            'content': self.content,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'visible': self.visible
        }
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    
    def get_all_reviews(self):
        return self.query.filter_by(visible=True).all()
    

    def get_review_by_id(self, public_id):
        return self.query.filter_by(public_id=public_id, visible=True).first()
    

    def create_review(self, data):
        review = Review(
            public_id=str(uuid.uuid4()),
            # user_id=data.get('user_id'),
            # category_id=data.get('category_id'),
            # region_id=data.get('region_id'),
            title=data.get('title'),
            content=data.get('content'),
            location=data.get('location'),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        review.save()
        return review
    

    def update_review(self, public_id, data):
        review = self.get_review_by_id(public_id)
        if not review:
            return None
        else:
            review.category_id = data.get('category_id')
            review.region_id = data.get('region_id')
            review.title = data.get('title')
            review.content = data.get('content')
            review.location = data.get('location')
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review
