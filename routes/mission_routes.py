from fastapi import APIRouter

from database.mission_db import mission_db
from utils.missions_helper import is_parmeters_exists, is_one_digit, is_number, is_id_exists, is_status_new, is_active
from utils.agents_helper import is_id_exists as is_id_agent_exists

route = APIRouter()


@route.post("")
def create_new_mission(data_from_user: dict):
    is_parmeters_exists(data_from_user)
    difficulty = data_from_user["difficulty"]
    importance = data_from_user["importance"]
    is_one_digit(difficulty)
    is_one_digit(importance)
    msg = mission_db.create_mission(data_from_user)
    return {"message": msg, "data": []}


@route.get("")
def get_all_missions():
    result = mission_db.get_all_missions()
    return {"message": "all missions", "data": result}


@route.get("/{id}")
def get_mission_by_id(id: int):
    is_number(id)
    is_id_exists(id)
    reault = mission_db.get_mission_by_id(id)
    return {"message": f"mission - {id}", "data": reault}


@route.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    is_number(id)
    is_number(agent_id)
    is_id_exists(id)
    is_id_agent_exists(agent_id)
    is_status_new(id)
    is_active(agent_id)
    pass
