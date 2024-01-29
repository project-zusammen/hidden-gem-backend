import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time

# from .Report import Report


class Appeal(db.Model):
    __tablename__ = "appeal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Need Reviewed")

    def __repr__(self):
        return f"<Appeal(reason={self.reason})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        # report_model = Report()
        # report_id = report_model.get_report_public_id(self.report_id)
        return {
            "public_id": self.public_id,
            # 'user_id': self.user_id,
            # 'report_id': self.appeal_id,
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
            self.public_id = str(uuid.uuid4())

            # report_public_id = data.get("item_id")
            # report_model = Report()
            # report = report_model.get_report_by_id(report_public_id)
            # self.item_id = report.id

            self.reason = data.get("reason")
            if not self.reason:
                raise Exception("Appeal explanation is required")
            
            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()
            self.status = "Need Reviewed"

            self.save()
            return self.serialize()
        except Exception as e:
            raise e
        
    def get_all_appeals(self):
        try:
            appeals = self.query.filter_by(visible=True).all()
            return [appeal.serialize() for appeal in appeals]
        except Exception as e:
            raise e
