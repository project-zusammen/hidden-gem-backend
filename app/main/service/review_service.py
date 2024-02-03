import logging as log
from app.main.model.review import Review
from app.main.model.tag import Tag, ReviewTag

review_model = Review()
tag_model = Tag()
review_tag_model = ReviewTag()


def create_review(data):
    try:
        review = review_model.create_review(data)
        # review_id = review_model.get_review_id_by_public_id(review["public_id"])
        # hashtags = review_model.get_the_hashtag_from_content(review["content"])
        # for hashtag in hashtags:
        #     tag = tag_model.create_tag(hashtag)
        #     result = review_tag_model.create_review_tag(tag["id"], review_id)
        response_object = {
            "status": "success",
            "message": "Successfully created.",
            "data": review,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in create_review: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def update_review(public_id, data):
    try:
        updated_review = review_model.update_review(public_id, data)
        if not update_review:
            response_object = {"status": "fail", "message": "Review does not exist."}
            return response_object, 409
        else:
            response_object = {
                "status": "success",
                "message": "Successfully updated.",
                "data": updated_review,
            }
            return response_object, 201
    except Exception as e:
        log.error(f"Error in update_review: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def upvote_review(public_id, upvote=True):
    try:
        updated_review = review_model.upvote_review(public_id, upvote)
        if not updated_review:
            response_object = {"status": "fail", "message": "Review does not exist."}
            return response_object, 409

        response_object = {
            "status": "success",
            "message": "Successfully upvoted.",
            "data": updated_review,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in upvote_review: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def update_visibility(public_id, visible=True):
    try:
        updated_visibility = review_model.update_visibility(public_id, visible)
        if not updated_visibility:
            response_object = {"status": "fail", "message": "Review does not exist."}
            return response_object, 409

        response_object = {
            "status": "success",
            "message": "Successfully updated.",
            "data": updated_visibility,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in update_visibility: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def get_all_reviews(page, count, tag_id, category_id, region_id):
    try:
        reviews = review_model.get_all_reviews(
            page, count, tag_id, category_id, region_id
        )
        if not reviews:
            return {"status": "success", "message": "No reviews found", "data": []}, 200

        response_object = {
            "status": "success",
            "message": "Successfully retrieved reviews.",
            "data": reviews,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_all_reviews: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def get_a_review(public_id):
    try:
        review = review_model.get_review_by_id(public_id)
        if not review:
            response_object = {"status": "fail", "message": "Review does not exist."}
            return response_object, 409

        response_object = {
            "status": "success",
            "message": "Successfully get a review.",
            "data": review,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get_a_review: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def delete_review(public_id):
    try:
        review = review_model.delete_review(public_id)
        if not review:
            response_object = {"status": "fail", "message": "Review does not exist."}
            return response_object, 409
        response_object = {
            "status": "success",
            "message": "Successfully deleted.",
            "data": review,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in delete_review: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500
