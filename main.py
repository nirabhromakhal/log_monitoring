import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from log_utils import add_log, query_logs
from models import LogInput, QueryInput, Log, LogMetadata

app = FastAPI(middleware=[Middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)])


@app.post("/add")
def add_log_(log: LogInput):
    add_log.delay(log.dict())


@app.post("/query", response_model=list[LogInput])
def query_logs_(query: QueryInput, limit: int = 100, offset: int = 0):
    logs: list[Log] = query_logs(query, limit, offset)
    return [
        LogInput(
            level=log.level,
            message=log.message,
            resourceId=log.resourceId,
            timestamp=log.timestamp,
            traceId=log.traceId,
            spanId=log.spanId,
            commit=log.commit,
            metadata=LogMetadata(
                parentResourceId=log.metadata_["parentResourceId"]
            )
        )
        for log in logs
    ]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
