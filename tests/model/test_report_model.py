import datetime
import unittest
from app.extensions import db
from app.main import create_app
from app.main.model.report import Report
from app.main.model.review import Review
from app.main.model.region import Region
from app.main.model.user import User
from app.main.model.comment import Comment

def setup_data():
    global reviewer, review, reporter, admin, comment, reporter_2

    region = Region(
        public_id = "region_id",
        city = "Test Region City",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    region.save()

    reviewer = User(
        username = "test_reviewer",
        email = "test_reviewer@gmail.com",
        password = "test_reviewer_password",
        role = "user",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    reviewer.save()

    review = Review(
        public_id = "review_id",
        title = "Test Review",
        content = "This is a test review.",
        location = "Test Location",
        region_id = region.id,
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
        upvotes = 0,
        downvotes = 0,
        visible = True,
    )
    review.save()

    reporter = User(
        username = "test_reporter",
        email = "test_reporter@gmail.com",
        password = "test_reporter_password",
        role = "user",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    reporter.save()

    admin = User(
        username = "test_admin",
        email = "test_admin@gmail.com",
        password = "test_admin_password",
        role = "admin",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    admin.save()
    
    comment = Comment(
        public_id = "comment_id",
        content = "This is a test comment.",
        review_id = review.id,
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    comment.save()

    reporter_2 = User(
        username = "test_reporter_2",
        email = "test_reporter_2@gmail.com",
        password = "test_reporter_2_password",
        role = "user",
        status = "active",
        created_at = datetime.datetime.utcnow(),
        updated_at = datetime.datetime.utcnow(),
    )
    reporter_2.save()

review_data = {
    "title": "Test Review",
    "content": "This is a test review.",
    "location": "Test Location",
}

report_data = {
    "reason": "Test Reason",
    "status": "received",
}

def register_user():
    global user_id, user_role
    user_data = {
        "username": "test_users",
        "email": "test_users@gmail.com",
        "password": "test_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    user_id = user_model.get_user_id(user["public_id"])
    user_role = user_model.get_user_role(user["public_id"])

def register_admin():
    global admin_id, admin_role
    user_data = {
        "username": "test_admins",
        "email": "test_admins@gmail.com",
        "password": "test_admin_password",
    }
    user_model = User()
    admin = user_model.register_admin(user_data)
    admin_id = user_model.get_user_id(admin["public_id"])
    admin_role = user_model.get_user_role(admin["public_id"])

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
    global reporter_id, user_id, user_role
    user_data = {
        "username": "test_reporter",
        "email": "test_reporter@gmail.com",
        "password": "test_reporter_password",
    }
    user_model = User()
    user = user_model.register_user(user_data)
    user_id = user_model.get_user_id(user["public_id"])
    user_role = user_model.get_user_role(user["public_id"])
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
        setup_data()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_get_report_on_review(self):
        # ARRANGE
        report_model = Report()
        report_data["type"] = "review"
        report_data["item_id"] = review.public_id
        report_data["user_id"] = reporter.id

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
        report_model = Report()
        report_data["type"] = "comment"
        report_data["item_id"] = comment.public_id
        report_data["user_id"] = reporter.id
        
        # ACT
        created_report = report_model.create_report(report_data)

        # ASSERT
        self.assertIsNotNone(created_report)
        self.assertEqual(created_report["type"], report_data["type"])
        self.assertEqual(created_report["item_id"], report_data["item_id"])
        self.assertEqual(created_report["reason"], report_data["reason"])
        self.assertEqual(created_report["status"], report_data["status"])

    def test_get_all_reports(self):
        # ARRANGE
        report_model = Report()
        report_data_1 = report_data.copy()
        report_data_1["type"] = "review"
        report_data_1["item_id"] = review.public_id
        report_data_1["user_id"] = reporter.id
        report_model.create_report(report_data_1)

        report_data_2 = report_data.copy()
        report_data_2["type"] = "comment"
        report_data_2["item_id"] = comment.public_id
        report_data_2["user_id"] = reporter.id
        report_model.create_report(report_data_2)
        
        # ACT
        all_reports = report_model.get_all_reports()

        # ASSERT
        self.assertIsNotNone(all_reports)
        self.assertEqual(len(all_reports), 2)
        self.assertEqual(all_reports[0]["type"], report_data_1["type"])
        self.assertEqual(all_reports[0]["item_id"], report_data_1["item_id"])
        self.assertEqual(all_reports[0]["reason"], report_data_1["reason"])
        self.assertEqual(all_reports[0]["status"], report_data_1["status"])
        self.assertEqual(all_reports[1]["type"], report_data_2["type"])
        self.assertEqual(all_reports[1]["item_id"], report_data_2["item_id"])
        self.assertEqual(all_reports[1]["reason"], report_data_2["reason"])
        self.assertEqual(all_reports[1]["status"], report_data_2["status"])

    def test_get_report_by_id_role_admin(self):
        # ARRANGE
        report_model = Report()
        report_data["type"] = "review"
        report_data["item_id"] = review.public_id
        report_data["user_id"] = reporter.id

        created_report = report_model.create_report(report_data)

        # ACT
        retrieved_report = report_model.get_report_by_id(
            public_id=created_report["public_id"], role=admin.role, user_id=None
        )

        # ASSERT
        self.assertIsNotNone(retrieved_report)
        self.assertEqual(retrieved_report["public_id"], created_report["public_id"])
        self.assertEqual(retrieved_report["type"], report_data["type"])
        self.assertEqual(retrieved_report["item_id"], report_data["item_id"])
        self.assertEqual(retrieved_report["reason"], report_data["reason"])
        self.assertEqual(retrieved_report["status"], report_data["status"])

    def test_get_report_by_id_role_user(self):
        # ARRANGE
        report_model = Report()
        report_data["type"] = "review"
        report_data["item_id"] = review.public_id
        report_data["user_id"] = reporter.id

        created_report = report_model.create_report(report_data)

        # ACT
        retrieved_report = report_model.get_report_by_id(
            public_id=created_report["public_id"], user_id=reporter.id, role=reporter.role
        )

        # ASSERT
        self.assertIsNotNone(retrieved_report)
        self.assertEqual(retrieved_report["public_id"], created_report["public_id"])
        self.assertEqual(retrieved_report["type"], report_data["type"])
        self.assertEqual(retrieved_report["item_id"], report_data["item_id"])
        self.assertEqual(retrieved_report["reason"], report_data["reason"])
        self.assertEqual(retrieved_report["status"], report_data["status"])

    def test_get_report_failed(self):
        # ARRANGE
        report_model = Report()
        report_data["type"] = "review"
        report_data["item_id"] = review.public_id
        report_data["user_id"] = reviewer.id

        report = report_model.create_report(report_data)

        # ASSERT
        with self.assertRaises(Exception) as context:
            report_model.get_report_by_id(
                public_id=report["public_id"], user_id=reporter_2.id, role=reporter_2.role
            )

        self.assertTrue("Access Denied" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
