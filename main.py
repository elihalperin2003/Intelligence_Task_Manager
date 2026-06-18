from fastapi import FastAPI

from routes.agent_routes import route as agent_route

app = FastAPI()

app.include_router(agent_route, prefix="/agents")


from database.agent_db import agent_db

print(agent_db.get_agent_by_id("999"))
