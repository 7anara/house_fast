from pydantic import BaseModel, EmailStr
from .models import RoleChoices, PropertyType, ConditionType
from typing import Optional
from datetime import date

class UserInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    status: Optional[RoleChoices]
    phone_number: Optional[str]
    avatar: Optional[str]

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    age: Optional[int]
    status: Optional[RoleChoices]
    phone_number: Optional[str]
    avatar: Optional[str]
    created_date: date

class CountryInputSchema(BaseModel):
    country_name: str

class CountryOutSchema(BaseModel):
    id: int
    country_name: str

class RegionInputSchema(BaseModel):
    country_id: int
    region_name: str

class RegionOutSchema(BaseModel):
    id: int
    country_id: int
    region_name: str

class CityInputSchema(BaseModel):
    region_id: int
    city_name: str
    city_image: Optional[str]

class CityOutSchema(BaseModel):
    id: int
    region_id: int
    city_name: str
    city_image: Optional[str]

class DistrictInputSchema(BaseModel):
    city_id: int
    district_name: str

class DistrictOutSchema(BaseModel):
    id: int
    city_id: int
    district_name: str

class PropertyInputSchema(BaseModel):
    title: str
    description: Optional[str]
    property_type: PropertyType
    seller_id: int
    region_id: int
    city_id: int
    district_id: int
    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floors: int
    condition: ConditionType
    documents: bool

class PropertyOutSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    property_type: PropertyType
    seller_id: int
    region_id: int
    city_id: int
    district_id: int
    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floors: int
    condition: ConditionType
    documents: bool

class PropertyInputImageSchema(BaseModel):
    property_id: int
    property_image: Optional[str]

class PropertyOutImageSchema(BaseModel):
    id: int
    property_id: int
    property_image: Optional[str]

class ReviewInputSchema(BaseModel):
    author_id: int
    seller_id: int
    rating: Optional[int]
    comment: Optional[str]

class ReviewOutSchema(BaseModel):
    id: int
    author_id: int
    seller_id: int
    rating: Optional[int]
    comment: Optional[str]

class HousePredictSchema(BaseModel):
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: str