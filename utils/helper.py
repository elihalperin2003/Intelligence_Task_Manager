from fastapi import HTTPException


def is_id_number(id):
    if not isinstance(id, int):
        raise HTTPException(status_code=422, detail=f"{id} - Not number")


def is_id_exists(data, id):
    if not data:
        raise HTTPException(status_code=404, detail=f"{id} - Not found")
