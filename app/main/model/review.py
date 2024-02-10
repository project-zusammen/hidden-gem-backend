import uuid
import logging
import datetime
from .. import db
from ..util.helper import convert_to_local_time
from .user import User 
from .region import Region
from .category import Category
from .tag import Tag

region_model = Region()
user_model = User()
category_model = Category()
tag_model = Tag()

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
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tag.id", name="fk_review_tag")
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
        
        region_public_id = region_model.get_region_public_id(self.region_id)
        user_public_id = user_model.get_user_public_id(self.user_id)
        category_public_id = category_model.get_public_id(self.category_id)
        tag_public_id = tag_model.get_tag_public_id(self.tag_id)

        return {
            "public_id": self.public_id,
            'user_id': user_public_id,
            'category_id': category_public_id,
            "region_id": region_public_id,
            "tag_id": tag_public_id,
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

    def get_all_reviews(self, page, count, region_id, category_id, tag_id):
        try:
            offset = (page - 1) * count
            query = self.query.filter(Review.visible == True)
            if tag_id:
                tag_db_id = tag_model.get_tag_db_id(tag_id)
                query = query.filter(Review.tag_id == tag_db_id)
            if category_id:
                category_db_id = category_model.get_category_id(category_id)
                query = query.filter(Review.category_id == category_db_id)
            if region_id:
                region_db_id = region_model.get_region_by_id(region_id)
                query = query.filter(Review.region_id == region_db_id)

            reviews = query.limit(count).offset(offset).all()
            return [review.serialize() for review in reviews]
        except Exception as e:
            logging.exception("An error occurred while creating a report: %s", str(e))
            return None

    def get_review_by_id(self, public_id):
        review = self.query.filter_by(public_id=public_id, visible=True).first()
        if review:
            return review.serialize()
        return None
    
    def get_review_public_id(self, id):
        review = self.query.filter_by(id=id).first()
        if review:
            return review.public_id
        return None

    def create_review(self, data):
        try:
            self.public_id = str(uuid.uuid4())
            self.location = data.get("location")
            
            self.title = data.get("title")
            self.content = data.get("content")
            if not self.title or not self.content:
                return None

            user_id = data.get("user_id")
            if user_id:
                user_model = User()
                self.user_id = user_model.get_user_id(user_id)
            
            category_id = data.get("category_id")
            if category_id:
                category_model = Category()
                self.category_id = category_model.get_category_id(category_id)

            region_id = data.get("region_id")
            if region_id:
                region_model = Region()
                self.region_id = region_model.get_region_by_id(region_id)
            
            tag_id = data.get("tag_id")
            if tag_id:
                tag_model = Tag()
                self.tag_id = tag_model.get_tag_db_id(tag_id)

            self.created_at = datetime.datetime.utcnow()
            self.updated_at = datetime.datetime.utcnow()
            self.upvotes = 0
            self.downvotes = 0
            self.visible = True

            self.save()
            return self.serialize()
        except Exception as e:
            logging.exception("An error occurred while creating a report: %s", str(e))
            return None

    def update_review(self, public_id, data):
        review = self.query.filter_by(public_id=public_id, visible=True).first()
        if not review:
            return None
        else:
            region_id = data.get("region_id")
            if region_id:
                region_model = Region()
                review.region_id = region_model.get_region_by_id(region_id)
            
            review.title = data.get("title")
            review.content = data.get("content")
            review.location = data.get("location")
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review.serialize()

    def delete_review(self, public_id):
        review = self.query.filter_by(public_id=public_id, visible=True).first()
        if not review:
            return None
        else:
            review.visible = False
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review.serialize()

    def upvote_review(self, public_id, upvote=True):
        review = self.query.filter_by(public_id=public_id, visible=True).first()
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
        review = self.query.filter_by(public_id=public_id, visible=True).first()
        if not review:
            return None
        else:
            review.visible = visible
            review.updated_at = datetime.datetime.utcnow()
            review.save()
            return review.serialize()

    def get_review_db_id(self, public_id):
        review = self.query.filter_by(public_id=public_id).first()
        if review:
            return review.id
        return None