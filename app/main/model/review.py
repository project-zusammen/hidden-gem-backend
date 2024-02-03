import uuid
import datetime
from .. import db
from ..util.helper import convert_to_local_time
import re
from .tag import ReviewTag



class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", name="fk_review_user"), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id", name="fk_review_category")
    )
    region_id = db.Column(
        db.Integer, db.ForeignKey("region.id", name="fk_review_region"), nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    visible = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Review(title={self.title}, content={self.content}), upvotes={self.upvotes}, downvotes={self.downvotes}>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "region_id": self.region_id,
            "title": self.title,
            "content": self.content,
            "location": self.location,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "visible": self.visible,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all_reviews(self, page, count, tag_id, category_id, region_id):
        try:
            offset = (page - 1) * count
            query = db.session.query(Review).join(
                ReviewTag, ReviewTag.review_id == Review.id, isouter=True
            )
            query = query.filter(Review.visible == True)
            if tag_id:
                query = query.filter(ReviewTag.tag_id == tag_id)
            if category_id:
                query = query.filter(Review.category_id == category_id)
            if region_id:
                query = query.filter(Review.region_id == region_id)

            reviews = query.limit(count).offset(offset).all()
            return [review.serialize() for review in reviews]
        except Exception as e:
            raise e

    def get_review_by_id(self, public_id):
        return self.query.filter_by(public_id=public_id, visible=True).first()

    def create_review(self, data):
        self.public_id = str(uuid.uuid4())
        self.title = data.get("title")
        self.content = data.get("content")
        self.location = data.get("location")
        self.user_id = data.get("user_id")
        self.category_id = data.get("category_id")
        self.region_id = data.get("region_id")
        if not self.title or not self.content:
            return None

        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        self.upvotes = 0
        self.downvotes = 0
        self.visible = True

        self.save()
        return self.serialize()

    def update_review(self, public_id, data):
        review = self.get_review_by_id(public_id)
        if not review:
            return None
        else:
            review.category_id = data.get("category_id")
            review.region_id = data.get("region_id")
            review.title = data.get("title")
            review.content = data.get("content")
            review.location = data.get("location")
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review.serialize()

    def delete_review(self, public_id):
        review = self.get_review_by_id(public_id)
        if not review:
            return None
        else:
            review.visible = False
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review.serialize()

    def upvote_review(self, public_id, upvote=True):
        review = self.get_review_by_id(public_id)
        if not review:
            return None
        if upvote:
            review.upvotes += 1
        else:
            review.downvotes += 1
        review.updated_at = datetime.datetime.utcnow()
        review.save()
        return review.serialize()

    def update_visibility(self, public_id, visible=True):
        review = self.get_review_by_id(public_id)
        if not review:
            return None
        else:
            review.visible = visible
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review.serialize()

    def get_review_id_by_public_id(self, public_id):
        try:
            review = self.query.filter_by(public_id=public_id, visible=True).first()
            if not review:
                raise Exception("Review not found. Invalid public_id")
            return review.id
        except Exception as e:
            raise e

    def get_the_hashtag_from_content(self, content):
        try:
            return re.findall(r"\#\w+", content)
        except Exception as e:
            raise e
