import unittest
from app.main import create_app
from app.extensions import db
from app.main.model.category import Category
from app.main.util.helper import create_token


category_data = {"name": "food"}


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="app.test_settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_category(self):
        # ARRANGE
        category_model = Category()
        new_category = category_model.create_category(category_data['name'])

        # ASSERT
        self.assertIsNotNone(new_category)
        self.assertEqual(new_category["name"], category_data["name"])


if __name__ == "__main__":
    unittest.main()
