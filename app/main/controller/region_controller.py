from ..util.dto import RegionDto

region_dto = RegionDto()
_region = region_dto.region

from flask_restx import Resource
from ..service.region_service import(
    get_all_region,
    create_region,
    update_region,
    delete_region
)

from ...extensions import ns

@ns.route("/region")
class RegionList(Resource):
    def get(self):
        """List all regions"""
        return get_all_region()
    
    @ns.expect(_region, validate=True)
    def post(self):
        """Create a new region"""

        return create_region(ns.payload.get("city"))
    
@ns.route("/region/<public_id>")
@ns.param("public_id", "The region identifier")
class RegionUpdate(Resource):
    @ns.expect(_region, validate=True)
    def put(self, public_id):
        """Update city name"""
        city_name = ns.payload.get("city")
        city_update = update_region(public_id,city_name)
        return city_update
    
    def delete(self, public_id):
        """Delete a region"""
        return delete_region(public_id)

