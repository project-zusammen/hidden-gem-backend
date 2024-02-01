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
            "id": self.id,
            "public_id": self.public_id,
            "name": self.name,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_tag(self, name):
        try:
            tag = self.query.filter_by(name=name).first()
            if tag:
                return {"id": tag.id}
            self.public_id = str(uuid.uuid4())
            self.name = name
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()

            self.save()
            return self.serialize()
        except Exception as e:
            raise e


class ReviewTag(db.Model):
    __tablename__ = "review_tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<ReviewTag(tag_id={self.tag_id}, review_id={self.review_id})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "tag_id": self.tag_id,
            "review_id": self.review_id,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_review_tag(self, tag_id, review_id):
        try:
            self.public_id = str(uuid.uuid4())
            self.tag_id = tag_id
            self.review_id = review_id
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()

            self.save()
            return self.serialize()
        except Exception as e:
            raise e
