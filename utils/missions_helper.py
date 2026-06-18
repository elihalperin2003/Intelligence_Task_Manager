from fastapi import HTTPException

from database.mission_db import mission_db
from database.agent_db import agent_db


def is_number(num):
    if not isinstance(num, int):
        raise HTTPException(status_code=422, detail=f"{num} - Not number")


def is_id_exists(id):
    if not mission_db.get_mission_by_id(id):
        raise HTTPException(status_code=404, detail=f"{id} - Not found")


def is_parmeters_exists(data_from_user: dict):
    if not data_from_user:
        raise HTTPException(status_code=422, detail="data Not exists")
    try:
        title = data_from_user["title"]
        description = data_from_user["description"]
        location = data_from_user["location"]
        difficulty = data_from_user["difficulty"]
        importance = data_from_user["importance"]
    except KeyError:
        raise HTTPException(status_code=422, detail="Required parameters - title, description, location, difficulty, importance")


def is_one_digit(num):
    is_number(num)
    if not (1 <= num <= 10):
        raise HTTPException(status_code=400, detail=f"{num} is not between 1 and 10")


def is_status(id, statuses):
    mission = mission_db.get_mission_by_id(id)
    if mission["status"] not in statuses:
        raise HTTPException(status_code=400, detail=f"{id} - Not in status {statuses}")


def is_active(id):
    if agent_db.get_agent_by_id(id)["is_active"] == False:
        raise HTTPException(status_code=400, detail=f"{id} - the agent is not active")


def is_more_three_missions(id):
    if mission_db.count_open_missions(id) >= 3:
        raise HTTPException(status_code=400, detail="There are 3 missions")


def is_critical(id_a, id_m):
    agent = agent_db.get_agent_by_id(id_a)
    mission = mission_db.get_mission_by_id(id_m)
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        raise HTTPException(status_code=400, detail="only Comandor can make missions in status CRITICAL!")
