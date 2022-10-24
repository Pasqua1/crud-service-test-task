from typing import List
from sqlalchemy.orm import Session

from model import Request, RequestTable

def get_request(db: Session, record_id: str) -> RequestTable:
    return db.query(RequestTable).filter(RequestTable.record_id == record_id).first()

def create_request(db: Session, request: Request):
    db_request: RequestTable = RequestTable(record_id = request.record_id,
                             record = request.record,
                             count = request.count)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def update_request(db: Session, request: RequestTable):
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def delete_request(db: Session, request: RequestTable):
    db.delete(request)
    db.commit()

def get_statistics(db: Session):
    requests: List[RequestTable] = db.query(RequestTable).filter(RequestTable.count > 0).all()
    request_count: int = 0
    unique_request_count: int = 0
    for request in requests:
        request_count += request.count
        unique_request_count += 1
    duplicates_percentage: float = (1 - unique_request_count/request_count)*100
    return round(duplicates_percentage, 2)
