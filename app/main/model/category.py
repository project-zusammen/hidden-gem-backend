from .. import db
import uuid
import datetime
from ..util.helper import convert_to_local_time

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Category(name={self.name})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "name": self.name,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def create_category(self, category_name):
        try:
            category = Category(
                public_id = str(uuid.uuid4()),
                name = category_name,
                created_at = datetime.datetime.utcnow(),
                updated_at = datetime.datetime.utcnow(),
            )

            category.save()
            return category.serialize()
        except Exception as e:
            raise e
