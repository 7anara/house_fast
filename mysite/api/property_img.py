from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import PropertyImages
from mysite.database.schema import PropertyInputImageSchema, PropertyOutImageSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

pro_img_router = APIRouter(prefix='/property_image', tags=['PropertyImage'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pro_img_router.post('/', response_model=PropertyOutImageSchema)
async def create_img(image: PropertyInputImageSchema, db: Session = Depends(get_db)):
    image_db = PropertyImages(**image.dict())

    db.add(image_db)
    db.commit()
    db.refresh(image_db)

    return image_db

@pro_img_router.get('/', response_model=List[PropertyOutImageSchema])
async def list_img(db: Session = Depends(get_db)):
    return db.query(PropertyImages).all()

@pro_img_router.get('/{img_id}', response_model=PropertyOutImageSchema)
async def detail_img(img_id: int, db: Session = Depends(get_db)):
    img_db = db.query(PropertyImages).filter(PropertyImages.id == img_id).first()
    if not img_db:
        raise HTTPException(detail='No such PropertyImages', status_code=400)

    return img_db

@pro_img_router.put('/{img_id}', response_model=dict)
async def update_img(image: PropertyInputImageSchema, img_id: int, db: Session = Depends(get_db)):
    img_db = db.query(PropertyImages).filter(PropertyImages.id == img_id).first()
    if not img_db:
        raise HTTPException(detail='No such PropertyImage', status_code=400)

    for key, value in image.dict().items():
        setattr(img_db, key, value)

    db.commit()
    db.refresh(img_db)

    return {'message': 'update PropertyImage'}

@pro_img_router.delete('/{img_id}', response_model=dict)
async def delete_img(img_id: int, db: Session = Depends(get_db)):
    img_db = db.query(PropertyImages).filter(PropertyImages.id == img_id).first()
    if not img_db:
        raise HTTPException(detail='No such PropertyImage', status_code=400)

    db.delete(img_db)
    db.commit()

    return {'message': 'message delete'}