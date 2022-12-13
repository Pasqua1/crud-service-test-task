from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from db import session
from model import RequestTable, Request

import base64

app = FastAPI()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def create_key(record: dict):
    request_key: str = ""
    for key, value in record.items():
        request_key += str(key) + str(value)
    request_key_base64 = base64.b64encode(bytes(request_key, 'utf-8'))
    return request_key_base64

@app.post("/fastapi/requests/", response_model = dict)
async def create_request(record: dict, db: Session = Depends(get_db)):
    key = create_key(record)
    db_request: RequestTable = crud.get_request(db, record_id = key)
    if db_request is not None:
        db_request.count += 1
        crud.update_request(db, db_request)
    else:
        request: Request = Request(record_id = key,
                                   record = record,
                                   count = 1)
        crud.create_request(db, request)
    return {"record_id" : key}

@app.get("/fastapi/requests/:key", response_model = dict)
async def get_request(key: str, db: Session = Depends(get_db)):
    db_request: Request = crud.get_request(db, record_id = key)
    if db_request is None:
        raise HTTPException(status_code=404,
                            detail="There is no record in database with record_id = " + key)
    db_request.record["duplicates"] = db_request.count - 1
    return db_request.record

@app.delete("/fastapi/requests/:key")
async def delete_request(key: str, db: Session = Depends(get_db)):
    db_request: RequestTable = crud.get_request(db, record_id = key)
    if db_request is None:
        raise HTTPException(status_code=404,
                            detail="There is no record in database with record_id = " + key)
    crud.delete_request(db, db_request)
    return HTTPException(status_code=200)

@app.put("/fastapi/requests/:key", response_model = dict)
async def put_request(key: str, record: dict, db: Session = Depends(get_db)):
    #check zz_bridge_v2 for understanding calling the method from url
    db_request: Request = crud.get_request(db, record_id = key)
    if db_request is None:
        raise HTTPException(status_code=404,
                            detail="There is no record in database with record_id = " + key)
    
    new_key = create_key(record)
    existing_request: Request = crud.get_request(db, record_id = new_key)
    if existing_request is not None:
        raise HTTPException(status_code=400,
                        detail="Request with this body have already exist")
    else:
        request: RequestTable = RequestTable(record_id = new_key,
                                                    record = record,
                                                    count = 1)
        crud.update_request(db, request)
        crud.delete_request(db, db_request)
    
    return {'request_id' :new_key}

@app.get("/fastapi/statistics/:key", response_model = dict)
async def get_statistics(db: Session = Depends(get_db)):
    return crud.get_statistics(db)