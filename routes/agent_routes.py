from fastapi import APIRouter

from database.agent_db import agent_db
from utils.helper import is_id_number, is_id_exists

route = APIRouter()


@route.post("")
def create_new_agent(data_from_user: dict):
    name = data_from_user["name"]
    specialty = data_from_user["specialty"]
    agent_rank = data_from_user["agent_rank"]
    data = {"name": name, "specialty": specialty, "agent_rank": agent_rank}
    msg = agent_db.create_agent()
    return {"message": msg, "data": data}


@route.get("")
def get_all_agents():
    msg = "all agents"
    data = agent_db.get_all_agents()
    return {"message": msg, "data": data}


@route.get("/{id}")
def get_agent_by_id(id: int):
    msg = f"agent - {id}"
    data = agent_db.get_agent_by_id(id)
    is_id_number(id)
    is_id_exists(data, id)
    return {"message": msg, "data": data}
