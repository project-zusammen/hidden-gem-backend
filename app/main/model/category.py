from .. import db
from sqlalchemy import func
import uuid
import datetime


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(
        db.String(100), unique=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f"<Category(name={self.name})>"

    def serialize(self):
        return {
            "public_id": self.public_id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_category(self, category_name):
        check_category = self.query.filter_by(name=category_name).first()
        if check_category:
            return check_category.serialize()
        try:
            self.public_id = str(uuid.uuid4())
            self.name = category_name
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()
            self.save()
            return self.serialize()
        except Exception as e:
            raise e
    
    def get_category_id(self, public_id):
        category = self.query.filter_by(public_id=public_id).first()
        if not category:
            return None
        return category.id
    
    def get_public_id(self, id):
        category = self.query.filter_by(id=id).first()
        if not category:
            return None
        return category.public_id
