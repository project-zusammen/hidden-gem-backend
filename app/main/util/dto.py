from flask_restx import Namespace, fields


class ReviewDto:
    api = Namespace('review', description='review related operations')
    review = api.model('review', {
        'title': fields.String(required=True, description='review title'),
        'content': fields.String(required=True, description='review content'),
        'location': fields.String(description='review location'),
        'category_id': fields.String(description='category Identifier'),
        'region_id': fields.String(description='region Identifier')
    })