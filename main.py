from mysite.api import user, city, country, region, property, property_img, district, review, predict, auth
import uvicorn
from mysite.admin.setup import setup_admin
from fastapi import FastAPI
from mysite.api.predict import predict_router


store = FastAPI()
store.include_router(user.user_router)
store.include_router(city.city_router)
store.include_router(country.country_router)
store.include_router(region.region_router)
store.include_router(property.property_router)
store.include_router(property_img.pro_img_router)
store.include_router(district.district_router)
store.include_router(predict_router)
store.include_router(review.review_router)
store.include_router(auth.auth_router)
setup_admin(store)



if __name__ == '__main__':
    uvicorn.run(store, host='127.0.0.1', port=8001)