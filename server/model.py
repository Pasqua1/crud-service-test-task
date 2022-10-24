from sqlalchemy import Column, Integer, String, JSON
from pydantic import BaseModel
from db import Base
from db import ENGINE


class RequestTable(Base):
    __tablename__ = "requests"
    record_id = Column(String(255), primary_key=True)
    record = Column(JSON)
    count = Column(Integer)


class Request(BaseModel):
    record_id: str
    record: dict
    count: int


    class Config:
        orm_mode = True


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
