from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine
from .views import (UserProfileAdmin, CityAdmin, CountryAdmin, PropertyAdmin, PropertyImagesAdmin, ReviewAdmin, DistrictAdmin, RegionAdmin)

def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(PropertyImagesAdmin)
    admin.add_view(DistrictAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(ReviewAdmin)