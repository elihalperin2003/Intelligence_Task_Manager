import mysql.connector

from db_connection import dB_connection

class AgentDB:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.connection.cursor
    
    def create_agent(self, name, specialty, agent_rank):
        with self.cursor() as cur:
            cur.execute(
                """
                INSERT INTO agents (name, specialty, agent_rank)
                VALUES (%s,%s,%s)
                """, (name,specialty,agent_rank)
            )
            self.conn.commit()
        return {"message": f"{name} - created successfully"}
    
    def get_all_agents(self):
        with self.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM agents")
            data = cur.fetchall()
        return data
    
    def get_agent_by_id(self, id):
        with self.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM agents WHERE id = %s", (id,))
            data = cur.fetchone()
        return data
    
    def update_agent(self, id, data:dict):
        
        keys = ", ".join(k for k in data.keys())
        values = tuple(k for k in data.values())
        sql_txt = f"UPDATE agents({keys}) VALUES("
        sql_txt += ", ".join(["%s" * len(values)])
        sql_txt += ") WHERE id = %s"
        print(sql_txt)
        # sql_txt = f"""
        #             UPDATE agents({keys})
        #             VALUES({", ".join("%s" * len(values))})
        #             WHERE id = f{"%s"}
        #             """
        with self.cursor(dictionary=True) as cur:
            cur.execute(sql_txt,(*values,id))
        return {"message": f"{id} - created successfully"}

    def deactivate_agent(self, id):
        with self.cursor() as cur:
            cur.execute("")
agent_db = AgentDB(dB_connection)

# print(agent_db.get_all_agents())
