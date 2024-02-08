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
    "status": "received",
}

def register_reviewer():
    global reviewer_id
    user_data = {
        "username": "test_reviewer",
        "email": "test_reviewer@gmail.com",
        "password": "test_reviewer_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    reviewer_id = user["public_id"]

def register_reporter():
    global reporter_id
    user_data = {
        "username": "test_reporter",
        "email": "test_reporter@gmail.com",
        "password": "test_reporter_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    reporter_id = user["public_id"]

def register_commenter():
    global commenter_id
    user_data = {
        "username": "test_commenter",
        "email": "test_commenter@gmail.com",
        "password": "test_commenter_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    commenter_id = user["public_id"]

class TestReport(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        register_reviewer()
        review_data["user_id"] = reviewer_id
        register_reporter()
        report_data["user_id"] = reporter_id        
    
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
        report_data["user_id"] = reporter_id
        
        # ACT
        created_report = report_model.create_report(report_data)

        # ASSERT
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report["type"], report_data["type"])
        self.assertEqual(created_report["item_id"], report_data["item_id"])
        self.assertEqual(created_report["reason"], report_data["reason"])
        self.assertEqual(created_report["status"], report_data["status"])
    
    def test_create_and_get_report_on_comment(self):
        # ARRANGE
        region_model = Region()
        created_region = region_model.create_region("Test Region")
        
        review_data["region_id"] = created_region["public_id"]
        review_model = Review()
        created_review = review_model.create_review(review_data)

        register_commenter()

        comment_data = {
            "content": "This is a test comment.",
            "review_id": created_review["public_id"],
            "user_id": commenter_id,
        }
        comment_model = Comment()
        created_comment = comment_model.create_comment(comment_data)
        
        report_model = Report()
        report_data["type"] = "comment"
        report_data["item_id"] = created_comment["public_id"]
        report_data["region_id"] = created_region["public_id"]
        report_data["user_id"] = reporter_id
        
        # ACT
        created_report = report_model.create_report(report_data)

        # ASSERT
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report["type"], report_data["type"])
        self.assertEqual(created_report["item_id"], report_data["item_id"])
        self.assertEqual(created_report["reason"], report_data["reason"])
        self.assertEqual(created_report["status"], report_data["status"])

if __name__ == "__main__":
    unittest.main()
