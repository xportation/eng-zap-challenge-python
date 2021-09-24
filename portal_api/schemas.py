from typing import List

from pydantic import BaseModel, Field

from portal_api.models import Property, BusinessType


class Pagination(BaseModel):
    class Config:
        allow_population_by_field_name = True

    page_number: int = Field(None, alias='pageNumber')
    page_size: int = Field(None, alias='pageSize')
    total_count: int = Field(None, alias='totalCount')
    listings: List[Property]


class Filter(BaseModel):
    class Config:
        allow_population_by_field_name = True

    business_type: BusinessType = Field(None, alias='businessType')
    city: str = None
    min_price: int = Field(None, alias='minPrice')
    max_price: int = Field(None, alias='maxPrice')
    bedrooms: int = None
    bathrooms: int = None
