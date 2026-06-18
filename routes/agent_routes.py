from fastapi import APIRouter

from database.agent_db import agent_db
from utils.helper import is_number, is_id_exists, is_arguments_correct, is_ramk_correct, is_parmeters_exists

route = APIRouter()


@route.post("")
def create_new_agent(data_from_user: dict):
    is_parmeters_exists(data_from_user)
    name = data_from_user["name"]
    specialty = data_from_user["specialty"]
    agent_rank = data_from_user["agent_rank"]
    is_ramk_correct(agent_rank)
    data = {"name": name, "specialty": specialty, "agent_rank": agent_rank}
    msg = agent_db.create_agent(data)
    return {"message": msg, "data": []}


@route.get("")
def get_all_agents():
    msg = "all agents"
    data = agent_db.get_all_agents()
    return {"message": msg, "data": data}


@route.get("/{id}")
def get_agent_by_id(id: int):
    is_number(id)
    is_id_exists(id)
    data = agent_db.get_agent_by_id(id)
    return {"message": f"agent - {id}", "data": data}


@route.put("/{id}")
def update_agent(id: int, data_from_user: dict):
    is_arguments_correct(data_from_user)
    is_number(id)
    is_id_exists(id)
    result = agent_db.update_agent(id, data_from_user)
    return {"message": result, "data": []}


@route.put("/{id}/deactivate")
def deactivate_agent(id: int):
    is_number(id)
    is_id_exists(id)
    result = agent_db.deactivate_agent(id)
    return {"message": result, "data": []}


@route.get("/{id}/performance")
def get_agent_performance(id: int):
    is_number(id)
    is_id_exists(id)
    result = agent_db.get_agent_performance(id)
    return {"message": f"{id} - performance", "data": result}
