import uuid
import unittest
import datetime
from app.main import create_app
from app.extensions import db
from app.main.model.tag import Tag
from app.main.model.user import User

tag_data = {"name": "This is a test tag"}


def register_user():
    global user_id, user_role
    user = User(
        public_id=str(uuid.uuid4()),
        username="test_user",
        email="test_user@mail.com",
        password="test_password",
        role="user",
        status="active",
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    user.save()
    user_id = user.public_id
    user_role = user.role


class TestTag(unittest.TestCase):
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

    def test_create_tag(self):
        # ARRANGE
        tag_model = Tag()

        # ACT
        new_tag = tag_model.create_tag(tag_data)

        # ASSERT
        self.assertIsNotNone(new_tag)
        self.assertEqual(new_tag["name"], tag_data["name"])
    
    def test_get_all_tags(self):
        # ARRANGE
        tag_model = Tag()
        tag_model.create_tag(tag_data)

        # ACT
        tags = tag_model.get_all_tags()

        # ASSERT
        self.assertIsNotNone(tags)
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]["name"], tag_data["name"])

if __name__ == "__main__":
    unittest.main()
