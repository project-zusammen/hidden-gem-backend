from .. import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


    def __init__(self, public_id, name, created_at, updated_at):
        self.public_id = public_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at


    def __repr__(self):
        return f"<Category(name={self.name})>"
    

    def serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
