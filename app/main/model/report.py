import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time
from .review import Review
from .comment import Comment
from .user import User
import logging


class Report(db.Model):
    __tablename__ = "report"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(100), nullable=False, default="received")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Report(type={self.type}, reason={self.reason})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)

        if self.type == "comment":
            comment_model = Comment()
            item_id = comment_model.get_comment_public_id(self.item_id)
        else:
            review_model = Review()
            item_id = review_model.get_review_public_id(self.item_id)

        user_model = User()
        user_public_id = user_model.get_user_public_id(self.user_id)

        return {
            "public_id": self.public_id,
            "user_id": user_public_id,
            "type": self.type,
            "item_id": item_id,
            "reason": self.reason,
            "status": self.status,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create_report(self, data):
        try:
            report_type = data.get("type")
            item_id = data.get("item_id")
            if report_type == "comment":
                comment_model = Comment()
                comment_id = comment_model.get_comment_db_id(item_id)
                item_id = comment_id
            else:
                review_model = Review()
                review_id = review_model.get_review_db_id(item_id)
                item_id = review_id

            report = Report(
                public_id=str(uuid.uuid4()),
                user_id=data.get("user_id"),
                type=report_type,
                status="received",
                item_id=item_id,
                reason=data.get("reason"),
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
            )

            report.save()
            return report.serialize()
        except Exception as e:
            raise e

    def get_all_reports(self, page, count):
        try:
            reports = self.query.order_by(Report.created_at.desc()).paginate(
                page=page, per_page=count, max_per_page=100, error_out=False
            )
            return [report.serialize() for report in reports]
        except Exception as e:
            raise e

    def get_report_by_id(self, public_id, role, user_id=None):
        try:
            report = self.query.filter_by(public_id=public_id).first()
            if not report:
                return None
            if role != "admin" and report.user_id != user_id:
                raise Exception("Access Denied")
            return report.serialize()
        except Exception as e:
            raise e

    def update_report(self, public_id, status):
        try:
            report = self.query.filter_by(public_id=public_id).first()
            if not report:
                return None
            report.updated_at = datetime.datetime.utcnow()
            report.status = status
            report.save()
            return report.serialize()
        except Exception as e:
            raise e
