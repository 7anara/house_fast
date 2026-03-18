from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import District
from mysite.database.schema import DistrictOutSchema, DistrictInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

district_router = APIRouter(prefix='/district', tags=['District'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@district_router.post('/', response_model=DistrictOutSchema)
async def create_dist(district: DistrictInputSchema, db: Session = Depends(get_db)):
    dist_db = District(**district.dict())

    db.add(dist_db)
    db.commit()
    db.refresh(dist_db)

    return dist_db

@district_router.get('/', response_model=List[DistrictOutSchema])
async def list_dict(db: Session = Depends(get_db)):
    return db.query(District).all()

@district_router.get('/{dist_id}', response_model=DistrictOutSchema)
async def detail_dict(dist_id: int, db: Session = Depends(get_db)):
    dist_db = db.query(District).filter(District.id == dist_id).first()
    if not dist_db:
        raise HTTPException(detail='No such District', status_code=400)

@district_router.put('/{dist_id}', response_model=dict)
async def update_dist(district: DistrictInputSchema, dist_id: int, db: Session = Depends(get_db)):
    dist_db = db.query(District).filter(District.id == dist_id).first()
    if not dist_db:
        raise HTTPException(detail='No such District', status_code=400)

    for key, value in district.dict().items():
        setattr(dist_db, key, value)

    db.commit()
    db.refresh(dist_db)

    return {'message': 'Changed District'}

@district_router.delete('/{dist_id}', response_model=dict)
async def delete_dist(dist_id: int, db: Session = Depends(get_db)):
    dist_db = db.query(District).filter(District.id == dist_id).first()
    if not dist_db:
        raise HTTPException(detail='No such', status_code=400)

    db.delete(dist_db)
    db.commit()

    return {'message': 'message delete'}
