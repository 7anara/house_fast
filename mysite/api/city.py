from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import City
from mysite.database.schema import CityOutSchema, CityInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


city_router = APIRouter(prefix='/city', tags=['City'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.post('/', response_model=CityOutSchema)
async def create_city(city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())

    db.add(city_db)
    db.commit()
    db.refresh(city_db)

    return city_db

@city_router.get('/', response_model=List[CityOutSchema])
async def list_city(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.get('/{city_id}', response_model=CityOutSchema)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(detail='No such City', status_code=400)

    return city_db

@city_router.put('/{city_id}', response_model=dict)
async def update_city(city_id: int, city: CityInputSchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
         raise HTTPException(detail='No such City', status_code=400)

    for key, value in city.dict().items():
        setattr(city_db, key, value)

    db.commit()
    db.refresh(city_db)

    return {'message': 'Changed City'}

@city_router.delete('/{city_id}', response_model=dict)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(detail='No such City', status_code=400)

    db.delete(city_db)
    db.commit()

    return {'message': 'message deleted'}

