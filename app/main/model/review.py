from .. import db

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    visible = db.Column(db.Boolean, nullable=False, default=True)


    def __init__(self, public_id, user_id, category_id, region_id, title, content, location, created_at, updated_at, upvotes, downvotes, visible):
        self.public_id = public_id
        self.user_id = user_id
        self.category_id = category_id
        self.region_id = region_id
        self.title = title
        self.content = content
        self.location = location
        self.created_at = created_at
        self.updated_at = updated_at
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.visible = visible
    

    def __repr__(self):
        return '<id {}>'.format(self.id)
    

    def serialize(self):
        return {
            'id': self.id,
            'public_id': self.public_id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'region_id': self.region_id,
            'title': self.title,
            'content': self.content,
            'location': self.location,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'visible': self.visible
        }
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
