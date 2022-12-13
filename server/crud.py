from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from model import Request, RequestTable

def get_request(db: Session, record_id: str) -> RequestTable:
    try:
        db_request = db.query(RequestTable).filter(RequestTable.record_id == record_id).first()
    except Exception as exp:
        raise HTTPException(status_code=503, detail=str(exp))
    return db_request

def create_request(db: Session, request: Request):
    try:
        db_request: RequestTable = RequestTable(record_id = request.record_id,
                                record = request.record,
                                count = request.count)
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
    except Exception as exp:
        raise HTTPException(status_code=503, detail=str(exp))
    return db_request

def update_request(db: Session, request: RequestTable):
    try:
        db.add(request)
        db.commit()
        db.refresh(request)
    except Exception as exp:
        raise HTTPException(status_code=503, detail=str(exp))
    return request

def delete_request(db: Session, request: RequestTable):
    try:
        db.delete(request)
        db.commit()
    except Exception as exp:
        raise HTTPException(status_code=503, detail=str(exp))

def get_statistics(db: Session):
    try:
        raws: int = db.query(RequestTable).count()
        if raws == 0:
            return {"duplicates_percentage": 0}
        duplicates = db.query(func.sum(RequestTable.count)).scalar()
        duplicates_percentage: float = (duplicates-raws)/duplicates
    except Exception as exp:
        raise HTTPException(status_code=503, detail=str(exp))
    return {"duplicates_percentage":round(duplicates_percentage, 2)}
