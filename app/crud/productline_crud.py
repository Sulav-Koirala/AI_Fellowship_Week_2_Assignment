from sqlalchemy.orm import Session
from app.models import ProductLine
from app.schemas.productline_schemas import ProductlineCreate, ProductlineUpdate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def get_product_lines(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ProductLine).offset(skip).limit(limit).all()

def get_product_line(db: Session, product_line: str):
    db_obj = db.query(ProductLine).filter(ProductLine.product_line == product_line).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="ProductLine not found")
    return db_obj

def create_product_line(db: Session, data: ProductlineCreate):
    db_obj = ProductLine(**data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_product_line(db: Session, product_line: str, data: ProductlineUpdate):
    db_obj = get_product_line(db, product_line)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_obj, key, value)
    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, 
            detail="ForeignKey Error"
        )


def delete_product_line(db: Session, product_line: str):
    db_obj = get_product_line(db, product_line)
    try:
        db.delete(db_obj)
        db.commit()
        return {"message": "Deleted"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, 
            detail="ForeignKey Error"
        )
    