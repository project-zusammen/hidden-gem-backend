import uuid
import datetime

from app.main import db
from app.main.model.comment import Comment

def get_all_comments():
    try:
        comments = Comment.query.filter_by(visible=True).all()
        if not comments:
            return {'status': 'success', 'message': 'No comment found', 'data': []}, 200

        comment_data = [comment.serialize() for comment in comments]

        response_object = {
            'status': 'success',
            'message': 'Successfully retrieved comments',
            'data': comment_data
        }
        return response_object, 200
    except Exception as e:
        print(f"Error in get_all_comments: {str(e)}")
        return {'status': 'error', 'message': 'Internal Server Error'}, 500
    
def create_comment(data):
    comment = Comment(
        public_id = str(uuid.uuid4()),
        # user_id = data.get('user_id'),
        review_id = data.get('review_id'),
        content = data.get('content'),
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow()
    )
    comment.save()
    response_object = {
        'status': 'success',
        'message': 'Successfully created.',
        'data': comment.serialize()
    }
    return response_object, 201