from sqlalchemy.orm import Session
from app.models import Office,Employee
from app.schemas.office_schemas import OfficeCreate, OfficeUpdate
from fastapi import HTTPException

def get_offices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Office).offset(skip).limit(limit).all()

def get_office(db: Session, office_code: str):
    office = db.query(Office).filter(Office.office_code == office_code).first()
    if not office:
        raise HTTPException(status_code=404, detail="Office not found")
    return office

def create_office(db: Session, data: OfficeCreate):
    db_office = Office(**data.model_dump())
    db.add(db_office)
    db.commit()
    db.refresh(db_office)
    return db_office

def update_office(db: Session, office_code: str, data: OfficeUpdate):
    db_office = get_office(db, office_code)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_office, key, value)
    db.commit()
    db.refresh(db_office)
    return db_office

def delete_office(db: Session, office_code: str):
    employee_count = db.query(Employee).filter(Employee.office_code == office_code).count()
    if employee_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete office. {employee_count} employees are still assigned to it."
        )
    db_office = db.query(Office).filter(Office.office_code == office_code).first()
    db.delete(db_office)
    db.commit()
    return {"message": "Office deleted successfully"}