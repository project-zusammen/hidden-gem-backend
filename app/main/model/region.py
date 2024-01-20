from .. import db

import uuid
import datetime
from ..util.helper import convert_to_local_time

class Region(db.Model):
    __tablename__ = "region"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, public_id, name, created_at, updated_at):
        self.public_id = public_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Region(name={self.name})>"

    def serialize(self):
        created_at = convert_to_local_time(self.created_at)
        updated_at = convert_to_local_time(self.updated_at)
        return {
            "public_id": self.public_id,
            "name": self.name,
            "created_at": created_at.isoformat() if self.created_at else None,
            "updated_at": updated_at.isoformat() if self.updated_at else None,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def create_region(self, region_name):
        try:
            self.public_id = str(uuid.uuid4())
            self.name = region_name

            self.save()
            return self.serialize()
        except Exception as e:
            raise e

    def get_all_regions(self):
        try:
            regions = self.query.all()
            return [regions.serialize() for region in regions]
        except Exception as e:
            raise e
        
    def get_region_by_id(self, public_id):
        return self.query.filter_by(public_id=public_id).first()
        
    def delete_region(self, public_id):
        try:
            region = self.get_region_by_id(public_id)
            if not region:
                raise Exception("Region not found")
            db.session.delete(region)
            db.session.commit()
            return True
        except Exception as e:
            raise e
    
    def update_region(self,public_id, new_region):
        try:
            region = self.get_region_by_id(public_id)
            if not region:
                raise Exception("Region not found")
            else:
                region.name = new_region
                region.updated_at = datetime.datetime.utcnow()

                db.session.commit()
                return region.serialize()

        except Exception as e:
            raise e
        