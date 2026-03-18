from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Region
from mysite.database.schema import RegionOutSchema, RegionInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

region_router = APIRouter(prefix='/region', tags=['Region'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@region_router.post('/', response_model=RegionOutSchema)
async def create_region(region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = Region(**region.dict())

    db.add(region_db)
    db.commit()
    db.refresh(region_db)

    return region_db

@region_router.get('/', response_model=List[RegionOutSchema])
async def list_region(db: Session = Depends(get_db)):
    return db.query(Region).all()

@region_router.get('/{region_id}', response_model=RegionOutSchema)
async def detail_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail='No such Region', status_code=400)

    return region_db

@region_router.put('/{region_id}', response_model=dict)
async def update_region(region: RegionInputSchema, region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail='No such region', status_code=400)

    for key, value in region.dict().items():
        setattr(region_db, key, value)

    db.commit()
    db.refresh(region_db)

    return {'message': 'update Region'}

@region_router.delete('/{region_id}', response_model=dict)
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail='No such Region', status_code=400)

    db.delete(region_db)
    db.commit()

    return {'message': 'deleted region'}
