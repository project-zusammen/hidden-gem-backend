from ..util.dto import CategoryDto
from flask_restx import Resource, Namespace
from ..service.category_service import (
    create_category,
    get_all_categories,
)

category_dto = CategoryDto()
_category = category_dto.category

ns = Namespace("category")

@ns.route("")
class CategoryList(Resource):
    @ns.expect(_category, validate=True)
    def post(self):
        """Create a new category"""
        return create_category(ns.payload.get("name"))
    
    def get(self):
        """Get a list of categories"""
        return get_all_categories()

