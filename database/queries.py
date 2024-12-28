from datetime import datetime, timedelta
import sqlite3
from typing import List, Tuple


class Database:
    def __init__(self, db_path: str = 'schedule_database.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY,
                team_name TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                member_id INTEGER PRIMARY KEY,
                team_id INTEGER,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (team_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shift_types (
                shift_type_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                schedule_id INTEGER PRIMARY KEY,
                team_id INTEGER,
                shift_type_id INTEGER,
                date DATE NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams (team_id)
                FOREIGN KEY (shift_type_id) REFERENCES shift_types (shift_type_id)
            )
        ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS member_shifts (
                        member_shift_id INTEGER PRIMARY KEY,
                        schedule_id INTEGER,
                        member_id INTEGER,
                        actual_start_time DATETIME,
                        actual_end_time DATETIME,
                        notes TEXT,
                        FOREIGN KEY (schedule_id) REFERENCES schedule (schedule_id),
                        FOREIGN KEY (member_id) REFERENCES team_members (member_id)
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS team_member_history (
                        history_id INTEGER PRIMARY KEY,
                        member_id INTEGER,
                        old_team_id INTEGER,
                        new_team_id INTEGER,
                        change_date DATETIME NOT NULL,
                        FOREIGN KEY (member_id) REFERENCES team_members (member_id),
                        FOREIGN KEY (old_team_id) REFERENCES teams (team_id),
                        FOREIGN KEY (new_team_id) REFERENCES teams (team_id)
                    )
                ''')

        self.conn.commit()


