from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Review
from mysite.database.schema import ReviewOutSchema, ReviewInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_router = APIRouter(prefix='/review', tags=['Review'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewOutSchema)
async def create_rev(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())

    db.add(review_db)
    db.commit()
    db.refresh(review_db)

    return review_db

@review_router.get('/', response_model=List[ReviewOutSchema])
async def list_rev(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get('/{rev_id}', response_model=ReviewOutSchema)
async def detail_rev(rev_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == rev_id).first()
    if not review_db:
        raise HTTPException(detail='No such Review', status_code=400)

    return review_db

@review_router.put('/{rev_id}', response_model=dict)
async def update_rev(review: ReviewInputSchema, rev_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == rev_id).first()
    if not review_db:
        raise HTTPException(detail='No such Review', status_code=400)

    for key, value in review.dict().items():
        setattr(review_db, key, value)

    return {'message': 'update review'}

@review_router.delete('/{rev_id}', response_model=dict)
async def delete_rev(rev_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == rev_id).first()
    if not review_db:
        raise HTTPException(detail='No such Review', status_code=400)

    db.delete(review_db)
    db.commit()

    return {'message': 'deleted review'}