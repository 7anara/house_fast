from mysite.database.models import (UserProfile, City, Country, Property, Review, PropertyImages, Region, District)
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [
        UserProfile.id,
        UserProfile.first_name,
        UserProfile.last_name,
        UserProfile.username,
        UserProfile.email,
        UserProfile.password,
        UserProfile.age,
        UserProfile.phone_number,
        UserProfile.status,
        UserProfile.avatar,
        UserProfile.created_date,

    ]
    name = 'user'
    name_plural = 'users'

class CountryAdmin(ModelView, model=Country):
    column_list = [
        Country.id,
        Country.country_name,
    ]

class RegionAdmin(ModelView, model=Region):
    column_list = [
        Region.id,
        Region.country_id,
        Region.region_name,
    ]

class CityAdmin(ModelView, model=City):
    column_list = [
        City.id,
        City.region_id,
        City.city_name,
        City.city_image,

    ]

class DistrictAdmin(ModelView, model=District):
    column_list = [
        District.id,
        District.city_id,
        District.district_name,
    ]


class PropertyAdmin(ModelView, model=Property):
    column_list = [
        Property.id,
        Property.title,
        Property.description,
        Property.property_type,
        Property.seller_id,
        Property.region_id,
        Property.city_id,
        Property.district_id,
        Property.address,
        Property.area,
        Property.price,
        Property.rooms,
        Property.floor,
        Property.total_floors,
        Property.condition,
        Property.documents,
    ]


class PropertyImagesAdmin(ModelView, model=PropertyImages):
    column_list = [
        PropertyImages.id,
        PropertyImages.property_id,
        PropertyImages.property_image,

    ]


class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id,
        Review.author_id,
        Review.seller_id,
        Review.rating,
        Review.comment,
    ]