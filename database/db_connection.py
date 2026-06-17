import mysql.connector

class DB_connection:
    def __init__(self):
        self.connection = None
        self.get_connection()
        self.create_database()
        self.create_tables()
    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
            )

    def create_database(self):
        with self.connection.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        self.connection.database = "Intelligence_db"
        self.commit()

    def create_tables(self):
        with self.connection.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS agents(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL,
                specialty VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE NOT NULL,
                completed_missions INT DEFAULT 0 NOT NULL,
                failed_missions INT DEFAULT 0 NOT NULL,
                agent_rank ENUM("Junior", "Senior", "Commander") NOT NULL
                )"""
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS missions(
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                location VARCHAR(50) NOT NULL,
                difficulty INT NOT NULL,
                importance INT NOT NULL,
                status ENUM("NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED")  NOT NULL,
                risk_level ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL"),
                assigned_agent_id INT DEFAULT NULL
                )"""
            )
        self.commit()

    def commit(self):
        if self.connection and self.connection.is_connected():
            self.connection.commit()
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()



dB_connection = DB_connection()
