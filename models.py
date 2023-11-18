from typing import Optional

from pydantic import BaseModel
from sqlalchemy import func, Integer, String, Column, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import declarative_base
from sqlalchemy_json import mutable_json_type

Base = declarative_base()


class LogMetadata(BaseModel):
    parentResourceId: str


class LogInput(BaseModel):
    level: str
    message: str
    resourceId: str
    timestamp: str
    traceId: str
    spanId: str
    commit: str
    metadata: LogMetadata


class QueryInput(BaseModel):
    search: str | None = None
    level: str | None = None
    resourceId: str | None = None
    timestamp_start: str | None = None
    timestamp_end: str | None = None
    traceId: str | None = None
    spanId: str | None = None
    commit: str | None = None
    metadata_parentResourceId: str | None = None


class Log(Base):
    __tablename__ = 'logs'
    id: Optional[int] = Column(Integer, primary_key=True)
    level = Column(String)
    message = Column(String)
    resourceId = Column(String)
    timestamp = Column(String)
    traceId = Column(String)
    spanId = Column(String)
    commit = Column(String)
    metadata_ = Column('metadata', mutable_json_type(dbtype=JSONB, nested=True))
    message_vector = Column(TSVECTOR, server_default=text("to_tsvector('english', message)"))






