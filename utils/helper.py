from fastapi import HTTPException

from database.agent_db import agent_db


def is_parmeters_exists(data_from_user: dict):
    try:
        name = data_from_user["name"]
        specialty = data_from_user["specialty"]
        agent_rank = data_from_user["agent_rank"]
    except KeyError:
        raise HTTPException(status_code=422, detail="Required parameters - name,specialty,agent rank")


def is_number(num):
    if not isinstance(num, int):
        raise HTTPException(status_code=422, detail=f"{num} - Not number")


def is_id_exists(id):
    if not agent_db.get_agent_by_id(id):
        raise HTTPException(status_code=404, detail=f"{id} - Not found")


def is_ramk_correct(rank):
    if rank not in ["Junior", "Senior", "Commander"]:
        raise HTTPException(status_code=400, detail=f"{rank} - Not a rank")


def is_arguments_correct(data: dict):
    if not data:
        raise HTTPException(status_code=422, detail="data Not exists")
    for key in data.keys():
        if key not in ["name", "specialty", "agent_rank"]:
            raise HTTPException(status_code=400, detail=f"{key} - is not parmeter")
    if data.get("agent_rank"):
        is_ramk_correct(data["agent_rank"])
