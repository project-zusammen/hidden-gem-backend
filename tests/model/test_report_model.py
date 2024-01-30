import uuid
import unittest
from app.extensions import db
from app.main import create_app
from app.main.model.report import Report
from app.main.model.review import Review
from app.main.model.region import Region
from app.main.model.user import User
from app.main.model.comment import Comment

review_data = {
    "title": "Test Review",
    "content": "This is a test review.",
    "location": "Test Location",
}

report_data = {
    "reason": "Test Reason",
}

def register_user():
    global user_id
    user_data = {
        "username": "test_user",
        "email": "test_user@gmail.com",
        "password": "test_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    user_id = user_model.get_user_id(user["public_id"])

class TestReport(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        register_user()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_get_report_on_review(self):
        # ARRANGE
        region_model = Region()
        created_region = region_model.create_region("Test Region")
        
        review_data["region_id"] = created_region["public_id"]
        review_model = Review()
        created_review = review_model.create_review(review_data)
        
        report_model = Report()
        report_data["type"] = "review"
        report_data["item_id"] = created_review["public_id"]
        report_data["region_id"] = created_region["public_id"]
        report_data["user_id"] = user_id
        
        # ACT
        created_report = report_model.create_report(report_data)

        # ASSERT
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report["type"], report_data["type"])
        self.assertEqual(created_report["item_id"], report_data["item_id"])
        self.assertEqual(created_report["reason"], report_data["reason"])
    
    def test_create_and_get_report_on_comment(self):
        # ARRANGE
        region_model = Region()
        created_region = region_model.create_region("Test Region")
        
        review_data["region_id"] = created_region["public_id"]
        review_model = Review()
        created_review = review_model.create_review(review_data)

        comment_data = {
            "content": "This is a test comment.",
            "review_id": created_review["public_id"],
        }
        comment_model = Comment()
        created_comment = comment_model.create_comment(comment_data)
        
        report_model = Report()
        report_data["type"] = "comment"
        report_data["item_id"] = created_comment["public_id"]
        report_data["region_id"] = created_region["public_id"]
        report_data["user_id"] = user_id
        
        # ACT
        created_report = report_model.create_report(report_data)

        # ASSERT
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report["type"], report_data["type"])
        self.assertEqual(created_report["item_id"], report_data["item_id"])
        self.assertEqual(created_report["reason"], report_data["reason"])

if __name__ == "__main__":
    unittest.main()
