import datetime
import enum
import math
from typing import List

from pydantic import BaseModel, Field


class Location(BaseModel):
    lon: float
    lat: float

    def is_valid(self):
        tolerance = 0.0000001
        return math.fabs(self.lat) > tolerance or math.fabs(self.lon) > tolerance


class GeoLocation(BaseModel):
    precision: str
    location: Location


class Address(BaseModel):
    class Config:
        allow_population_by_field_name = True

    city: str
    neighborhood: str
    geolocation: GeoLocation = Field(None, alias='geoLocation')


class BusinessType(str, enum.Enum):
    sale = 'SALE'
    rental = 'RENTAL'


class PricingInfo(BaseModel):
    class Config:
        allow_population_by_field_name = True

    period: str = None
    price: str
    rental_total_price: str = Field(None, alias='rentalTotalPrice')
    yearly_iptu: str = Field(None, alias='yearlyIptu')
    business_type: BusinessType = Field(None, alias='businessType')
    monthly_condo_fee: str = Field(None, alias='monthlyCondoFee')

    def get_monthly_condo_fee(self):
        try:
            return int(self.monthly_condo_fee)
        except (TypeError, ValueError):
            return 0


class Property(BaseModel):
    class Config:
        allow_population_by_field_name = True

    id: str
    owner: bool
    created_at: datetime.datetime = Field(None, alias='createdAt')
    updated_at: datetime.datetime = Field(None, alias='updatedAt')
    usable_areas: int = Field(None, alias='usableAreas')
    listing_type: str = Field(None, alias='listingType')
    listing_status: str = Field(None, alias='listingStatus')
    parking_spaces: str = Field(None, alias='parkingSpaces')
    images: List[str]
    bathrooms: int
    bedrooms: int
    address: Address
    pricing_info: PricingInfo = Field(None, alias='pricingInfos')


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
    address: str = None
    min_price: int = None
    max_price: int = None
    bedroom: int = None
    parking_space: int = None
    bathroom: int = None
