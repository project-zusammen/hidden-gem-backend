import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time
from .region import Region


class Image(db.Model):
    __tablename__ = "image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    review_id = db.Column(db.String(100), db.ForeignKey('review.id'), nullable=False)

    def __repr__(self):
        return f"<Image(url={self.url})>"
    
    def serialize(self):
        return {
            "url": self.url,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def get_images_by_review_id(self, review_id):
        images = self.query.filter_by(review_id=review_id).all()
        return [image.serialize() for image in images]