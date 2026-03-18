from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Country
from mysite.database.schema import CountryOutSchema, CountryInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

country_router = APIRouter(prefix='/country', tags=['Country'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@country_router.post('/', response_model=CountryOutSchema)
async def created_country(country: CountryInputSchema, db: Session = Depends(get_db)):
    country_db = Country(**country.dict())

    db.add(country_db)
    db.commit()
    db.refresh(country_db)

    return country_db

@country_router.get('/', response_model=List[CountryOutSchema])
async def list_country(db: Session = Depends(get_db)):
    return db.query(Country).all()

@country_router.get('/{count_id}', response_model=CountryOutSchema)
async def detail_country(count_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == count_id).first()
    if not country_db:
        raise HTTPException(detail='No such Country', status_code=400)

    return country_db

@country_router.put('/{count_id}', response_model=dict)
async def update_country(count_id: int, country: CountryInputSchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == count_id).first()
    if not country_db:
        raise HTTPException(detail='No such Country', status_code=400)

    for key, value in country.dict().items():
        setattr(country_db, key, value)

    db.commit()
    db.refresh(country_db)

@country_router.delete('/{count_id}', response_model=dict)
async def delete_country(count_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == count_id).first()
    if not country_db:
         raise HTTPException(detail='No such Country', status_code=400)

    db.delete(country_db)
    db.commit()

    return {'message': 'message delete'}