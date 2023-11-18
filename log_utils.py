from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from celery import Celery

from models import Log, QueryInput

postgres_connection_url = "postgresql://dyte:password@postgres/logs"
engine = create_engine(postgres_connection_url)
celery = Celery('tasks', broker='redis://redis:6379/0')


@celery.task
def add_log(log: dict):
    postgres_log = Log(
        **(log | {"metadata_": log["metadata"]})
    )
    with Session(engine) as session:
        session.add(postgres_log)
        session.commit()


def query_logs(query: QueryInput, limit: int, offset: int) -> list[Log]:
    with Session(engine) as session:
        sql = session.query(Log)
        if query.timestamp_start and query.timestamp_end:
            sql = sql.filter(Log.timestamp >= query.timestamp_start)
            sql = sql.filter(Log.timestamp <= query.timestamp_end)
        if query.search:
            search = query.search.replace("'", "''")
            sql = sql.filter(Log.message_vector.op('@@')(text(f"phraseto_tsquery('english', '{search}')")))
            sql = sql.filter(Log.message.ilike(f"%{search}%"))
        if query.level:
            sql = sql.filter(Log.level == query.level)
        if query.resourceId:
            sql = sql.filter(Log.resourceId == query.resourceId)
        if query.traceId:
            sql = sql.filter(Log.traceId == query.traceId)
        if query.spanId:
            sql = sql.filter(Log.spanId == query.spanId)
        if query.commit:
            sql = sql.filter(Log.commit == query.commit)
        if query.metadata_parentResourceId:
            sql = sql.filter(Log.metadata_['parentResourceId'].astext == query.metadata_parentResourceId)

        logs = sql.offset(offset).limit(limit).all()

    return list(logs)
