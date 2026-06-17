from db_connection import dB_connection

class AgentDB:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.connection.cursor
    
    def create_agent(self, data:dict):
        name = data["name"]
        specialty = data["specialty"]
        agent_rank = data["agent_rank"]
        with self.cursor() as cur:
            cur.execute(
                """
                INSERT INTO agents (name, specialty, agent_rank)
                VALUES (%s,%s,%s)
                """, (name,specialty,agent_rank)
            )
            self.conn.commit()
        return f"{name} - created successfully"
    
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
        keys = ", ".join(f"{k} = %s" for k in data.keys())
        values = tuple(v for v in data.values()) + (id,)
        with self.cursor(dictionary=True) as cur:
            cur.execute(
                f"""
                UPDATE agents
                SET {keys}
                WHERE id = {"%s"}
                """, (values)
            )
            self.conn.commit()
        return f"{id} - created successfully"

    def deactivate_agent(self, id):
        with self.cursor() as cur:
            cur.execute("UPDATE agents SET is_active = FALSE WHERE ID = %s", (id,))
            self.conn.commit()
        return f"{id} - deactivated successfully"
    
    def increment_completed(self,id):
        with self.cursor() as cur:
            cur.execute(
                """
                UPDATE agents
                SET completed_missions = completed_missions + 1
                WHERE ID = %s
                """, (id,)
            )
            self.conn.commit()
        return f"{id} - updated successfully"
    
    def increment_failed(self,id):
        with self.cursor() as cur:
            cur.execute(
                """
                UPDATE agents
                SET failed_missions = failed_missions + 1
                WHERE ID = %s
                """, (id,)
            )
            self.conn.commit()
        return f"{id} - updated successfully"

    # def get_agent_performance(self,id):
    #     total = 
    #     failed = 
    #     complated = 
    #     success_rate = round(complated / failed * 100,2)
    #     return {"total": total, "failed": failed, "complated": complated, "success_rate": success_rate}

    def count_active_agents(self):
        with self.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM agents
                WHERE is_active = TRUE
                """
            )
            data = cur.fetchone()
        return data[0]




agent_db = AgentDB(dB_connection)

print(agent_db.get_all_agents())
print(agent_db.create_agent({"name": "eli", "specialty":"soldier", "agent_rank": "Senior"}))
print(agent_db.get_all_agents())

#agent_db.update_agent(2,{"name": "lam", "specialty": "poops"})
