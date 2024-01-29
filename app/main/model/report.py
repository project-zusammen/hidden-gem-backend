import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time
from .review import Review
import logging

class Report(db.Model):
    __tablename__ = "report"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Report(type={self.type}, reason={self.reason})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        review_model = Review()
        item_id = review_model.get_review_public_id(self.item_id)

        return {
            "public_id": self.public_id,
            # 'user_id': self.user_id,
            "type": self.type,
            "item_id": item_id,
            "reason": self.reason,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_report(self, data):
        try:
            self.public_id = str(uuid.uuid4())
            self.user_id = data.get("user_id")
            self.type = data.get("type")
            
            review_public_id = data.get("item_id")
            review_model = Review()
            review = review_model.get_review_by_id(review_public_id)
            self.item_id = review.id
            
            self.reason = data.get("reason")
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()

            self.save()
            return self.serialize()
        except Exception as e:
            logging.exception("An error occurred while creating a report: %s", str(e))
            return None
