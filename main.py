from fastapi import FastAPI

from database.db_connection import dB_connection
from routes.agent_routes import route as agent_route
from routes.mission_routes import route as mission_route

dB_connection.get_connection()
dB_connection.create_database()
dB_connection.create_tables()

app = FastAPI()

app.include_router(agent_route, prefix="/agents")
app.include_router(mission_route, prefix="/missions")
