import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time

from .user import User


class Appeal(db.Model):
    __tablename__ = "appeal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="received")

    def __repr__(self):
        return f"<Appeal(reason={self.reason})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        user_model = User()
        user_public_id = user_model.get_user_public_id(self.user_id)
        # report_model = Report()
        # report_id = report_model.get_report_public_id(self.report_id)
        return {
            "public_id": self.public_id,
            "user_id": user_public_id,
            # 'report_id': self.report_id,
            "reason": self.reason,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
            "status": self.status,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_appeal(self, data):
        try:
            appeal = Appeal(
                public_id = str(uuid.uuid4()),
                user_id = data.get("user_id"),
                reason = data.get("reason"),
                created_at = datetime.datetime.utcnow(),
                updated_at = datetime.datetime.utcnow(),
                status = "received",
            )

            appeal.save()
            return appeal.serialize()
        except Exception as e:
            raise e

    def get_all_appeals(self):
        try:
            appeals = self.query.all()
            return [appeal.serialize() for appeal in appeals]
        except Exception as e:
            raise e

    def get_appeal_by_id(self, public_id, user_id, role):
        try:
            appeal = self.query.filter_by(public_id=public_id).first()
            if not appeal:
                return None
            if role != "admin" and appeal.user_id != user_id:
                raise Exception("Access Denied")
            return appeal.serialize()
        except Exception as e:
            raise e

    def update_appeal(self, public_id, status):
        try:
            appeal = self.query.filter_by(public_id=public_id).first()
            if not appeal:
                return None
            appeal.updated_at = datetime.datetime.utcnow()
            appeal.status = status
            appeal.save()
            return appeal.serialize()
        except Exception as e:
            raise e
