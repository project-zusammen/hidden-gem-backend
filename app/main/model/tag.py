from .. import db
import uuid
import datetime
from ..util.helper import convert_to_local_time


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Tag(name={self.name})>"

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

    def create_tag(self, data):
        try:
            tag = Tag(
                public_id=str(uuid.uuid4()),
                name=data.get('name'),
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
            )
            tag.save()
            return tag.serialize()
        except Exception as e:
            raise e
    
    def get_tag_db_id(self, public_id):
        try:
            tag = self.query.filter_by(public_id=public_id).first()
            if tag:
                return tag.id
            return None
        except Exception as e:
            raise e
        
    def get_tag_public_id(self, id):
        try:
            tag = self.query.filter_by(id=id).first()
            if tag:
                return tag.public_id
            return None
        except Exception as e:
            raise e
    
    def get_all_tags(self):
        try:
            tags = self.query.all()
            return [tag.serialize() for tag in tags]
        except Exception as e:
            raise e
        
