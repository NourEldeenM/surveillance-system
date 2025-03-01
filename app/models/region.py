from typing import List
from uuid import uuid4
from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import relationship, Mapped
from app.models.branch import Branch
from app.models.database import Base
from pydantic import BaseModel
import pycountry

class RegionLocation(BaseModel):
    full_name: str
    iso_code: str

    @classmethod
    def from_country_name(cls, country_name: str):
        """Creates a RegionLocation object from a country name."""
        country = pycountry.countries.get(name=country_name)
        if not country:
            raise ValueError(f"Invalid country name: {country_name}")
        return cls(full_name=country.name, iso_code=country.alpha_2)

    @classmethod
    def from_iso_code(cls, iso_code: str):
        """Creates a RegionLocation object from an ISO Alpha-2 country code."""
        country = pycountry.countries.get(alpha_2=iso_code.upper())
        if not country:
            raise ValueError(f"Invalid ISO code: {iso_code}")
        return cls(full_name=country.name, iso_code=country.alpha_2)

    
class Region(Base):
    __tablename__ = "regions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    region_location = Column(JSON, nullable=False)
    branches: Mapped[List["Branch"]] = relationship(back_populates="region")