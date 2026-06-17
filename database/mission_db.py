from db_connection import dB_connection

class MissionDB:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.connection.cursor

    def calculate_level(self, difficulty, importance):
       num = difficulty * 2 + importance
       if num <= 9:
           return "LOW"
       if 10 <= num <= 17:
           return "MEDIUM"
       if 18 <= num <= 24:
           return "HIGH"
       if 25 <= num:
           return "CRITICAL"
       return num

    def create_mission(self,data:dict):
        title = data["title"]
        description = data["description"]
        location = data["location"]
        difficulty = data["difficulty"]
        importance = data["importance"]
        risk_level = self.calculate_level(difficulty,importance)
        with self.cursor() as cur:
            cur.execute(
                """
                INSERT INTO missions (title, description, location, difficulty, importance, risk_level)
                VALUES (%s,%s,%s,%s,%s,%s)
                """, (title, description, location, difficulty, importance, risk_level)
            )
            self.conn.commit()
        return f"{title} - created successfully"
    
    def get_all_missions(self):
        with self.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM missions")
            data = cur.fetchall()
        return data
    
    def get_mission_by_id(self,id):
        with self.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM missions WHERE id = %s", (id,))
            data = cur.fetchone()
        return data
    
    def assign_mission(self, m_id, a_id):
        with self.cursor() as cur:
            cur.execute(
                """
                UPDATE missions
                SET assigned_agent_id = %s
                WHERE id = %s
                """, (a_id,m_id)
            )
            self.conn.commit()
        return f"{m_id} - updaed successfully"

    def update_mission_status(self,id, status):
        with self.cursor() as cur:
            cur.execute(   
                """
                UPDATE missions
                SET status = %s
                WHERE id = %s
                """, (status,id)
            )
            self.conn.commit()
        return f"{id} - status chenged to -{status}- successfully"
    
    def get_open_missions_by_agent(self, id):
        with self.cursor() as cur:
            cur.execute(
                """
                SELCET * FROM missions
                WHERE ssigned_agent_id = %s 
                AND (status = "ASSIGNED" OR status = "IN_PROGRESS")
                """, (id,)
            )
            data = cur.fetchall()
        return data
    
    def count_all_missions(self):
        return(len(self.get_all_missions()))
    
    def count_by_status(self,status):
        with self.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM missions
                WHERE status = %s
                """, (status,)
            )
            data = cur.fetchone()
        return data[0]
    
    def count_open_missions(self):
        with self.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM missions
                WHERE status IN ("NEW", "ASSIGNED", "IN_PROGRESS")
                """
            )
            data = cur.fetchone()
        return data[0]
    
    def count_critical_missions(self):
        with self.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM missions
                WHERE risk_level = "CRITICAL"
                """
            )
            data = cur.fetchone()
        return data[0]
    
    def get_top_agent(self):
        with self.cursor(dictionary=True) as cur:
            cur.execute(
                """
                SELECT * FROM agents
                ORDER BY completed_missions DESC LIMIT 1
                """
            )
            data = cur.fetchone()
        return data



# print(agent_db.get_all_agents())


mission_db = MissionDB(dB_connection)
print(mission_db.get_all_missions())
#print(mission_db.get_top_agent())
# # print(mission_db.get_mission_by_id(1))
# print(mission_db.get_open_missions_by_agent(1))
# print(mission_db.count_all_missions())
# print(mission_db.count_by_status("NEW"))
# print(mission_db.count_critical_missions())
#print(mission_db.create_mission({"title": "dream", "description": "to_dream", "location": "JLM", "difficulty": 9, "importance": 9}))
# print(mission_db.count_critical_missions())
