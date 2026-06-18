from fastapi import APIRouter

from database.mission_db import mission_db
from database.agent_db import agent_db
from utils.missions_helper import is_parmeters_exists, is_one_digit, is_number, is_id_exists, is_status, is_active, is_critical
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
    is_status(id, ["NEW"])
    is_active(agent_id)
    # is_more_three_missions()
    is_critical(agent_id, id)
    msg = mission_db.assign_mission(id, agent_id)
    mission_db.update_mission_status(id, "ASSIGNED")
    return {"message": msg, "data": []}


@route.put("/{id}/start")
def start_mission(id: int):
    is_number(id)
    is_id_exists(id)
    is_status(id, ["ASSIGNED"])
    msg = mission_db.update_mission_status(id, "IN_PROGRESS")
    return {"message": msg, "data": []}


@route.put("/{id}/complete")
def complete_mission(id: int):
    is_number(id)
    is_id_exists(id)
    is_status(id, ["IN_PROGRESS"])
    msg = mission_db.update_mission_status(id, "COMPLETED")
    agent = mission_db.get_mission_by_id(id).get("assigned_agent_id", 0)
    agent_db.increment_completed(agent_db.get_agent_by_id(agent)["id"])
    return {"message": msg, "data": []}


@route.put("/{id}/fail")
def fail_mission(id: int):
    is_number(id)
    is_id_exists(id)
    is_status(id, ["IN_PROGRESS"])
    msg = mission_db.update_mission_status(id, "FAILED")
    agent = mission_db.get_mission_by_id(id)["assigned_agent_id"]
    agent_db.increment_failed(agent_db.get_agent_by_id(agent)["id"])
    return {"message": msg, "data": []}


@route.put("/{id}/cancel")
def cancel_mission(id: int):
    is_number(id)
    is_id_exists(id)
    is_status(id, ["NEW", "ASSIGNED"])
    msg = mission_db.update_mission_status(id, "CANCELLED")
    return {"message": msg, "data": []}
