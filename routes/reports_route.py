from fastapi import APIRouter

from database.mission_db import mission_db

route = APIRouter()


@route.get("/top-agent")
def top_agent():
    data = mission_db.get_top_agent()
    return {"message": "The top agent", "data": data}


@route.get("/summary")
def get_summary():
    return {"message": "in the future", "data": []}


@route.get("/tmissions-by-status")
def get_tmissions_by_status():
    return {"message": "in the future", "data": []}
