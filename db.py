from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.database_url)
Session = sessionmaker(engine)

Base = declarative_base()


class DBEvent(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    name = Column(String)
    link = Column(String)
    organizer = Column(String)
    recurring = Column(Boolean)
    status = Column(String)
    google_id = Column(String)
    outlook_id = Column(String)


class Event(BaseModel):
    id: Optional[int]
    day: str
    start_date: datetime
    end_date: datetime
    name: str
    link: Optional[str]
    organizer: str
    recurring: bool
    status: str
    google_id: Optional[str]
    outlook_id: Optional[str]


def get_events_by_outlook_id(outlook_id: str):
    session = Session()
    return session.query(DBEvent).filter(DBEvent.outlook_id == outlook_id).first()


def get_events_with_out_google_id():
    session = Session()
    return session.query(DBEvent).filter(DBEvent.google_id == None).all()  # noqa


def update_google_id(event_id: int, google_id: str):
    session = Session()
    db_event = session.query(DBEvent).filter(DBEvent.id == event_id).first()
    db_event.google_id = google_id
    session.commit()
    session.refresh(db_event)
    return db_event


def create_event(event: Event):
    db_event = DBEvent(**event.dict())
    session = Session()
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


def update_event(event: Event):
    session = Session()
    db_event = session.query(DBEvent).filter(DBEvent.name == event.name).first()
    db_event.day = event.day
    db_event.start_date = event.start_date
    db_event.end_date = event.end_date
    db_event.link = event.link
    db_event.organizer = event.organizer
    db_event.status = event.status
    session.commit()
    session.refresh(db_event)
    return db_event


def search_event(name: str, day: str):
    session = Session()
    return (
        session.query(DBEvent).filter(DBEvent.name == name, DBEvent.day == day).first()
    )


Base.metadata.create_all(bind=engine)
