from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Property
from mysite.database.schema import PropertyOutSchema, PropertyInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

property_router = APIRouter(prefix='/property', tags=['Property'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@property_router.post('/', response_model=PropertyOutSchema)
async def create_pro(prop: PropertyInputSchema, db: Session = Depends(get_db)):
    pro_db = Property(**prop.dict())

    db.add(pro_db)
    db.commit()
    db.refresh(pro_db)

    return pro_db

@property_router.get('/', response_model=List[PropertyOutSchema])
async def list_pro(db: Session = Depends(get_db)):
    return db.query(Property).all()

@property_router.get('/{pro_id}', response_model=PropertyOutSchema)
async def detail_pro(pro_id: int, db: Session = Depends(get_db)):
    pro_db = db.query(Property).filter(Property.id == pro_id).first()
    if not pro_db:
        raise HTTPException(detail='No such Property', status_code=400)

    return pro_db

@property_router.put('/{pro_id}', response_model=dict)
async def update_pro(prop: PropertyInputSchema, pro_id: int, db: Session = Depends(get_db)):
    prop_db = db.query(Property).filter(Property.id == pro_id).first()
    if not prop_db:
        raise HTTPException(detail='No such Property', status_code=400)

    for key, value in prop.dict().items():
        setattr(prop_db, key, value)

    db.commit()
    db.refresh(prop_db)

    return {'message': 'update Property'}

@property_router.delete('/{pro_id}', response_model=dict)
async def delete_pro(pro_id: int, db: Session = Depends(get_db)):
    pro_db = db.query(Property).filter(Property.id == pro_id).first()
    if not pro_db:
        raise HTTPException(detail='No such Property', status_code=400)

    db.delete(pro_db)
    db.commit()

    return {'message': 'delete property'}