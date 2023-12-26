from flask_restx import fields
from app.extensions import api

"""
DTO (Data Transfer Object) is a simple object which is used to pass data between software components.
"""
class ReviewDto:
    review = api.model('review', {
        'title': fields.String(required=True, description='review title'),
        'content': fields.String(required=True, description='review content'),
        'location': fields.String(description='review location'),
        'category_id': fields.String(description='category Identifier'),
        'region_id': fields.String(description='region Identifier')
    })

class CommentDto:
    comment = api.model('comment', {
		'review_id': fields.String(required=True),
		'content': fields.String(required=True)
	})