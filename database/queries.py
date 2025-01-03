import os
from calendar import monthrange
from datetime import datetime, timedelta, date
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'schedule_database.db')


def setup_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            member_id INTEGER PRIMARY KEY,
            team_id INTEGER,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            role TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shift_types (
            shift_type_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            schedule_id INTEGER PRIMARY KEY,
            team_id INTEGER,
            shift_type_id INTEGER,
            date DATE NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
            FOREIGN KEY (shift_type_id) REFERENCES shift_types (shift_type_id)
        )
    ''')

    cursor.execute('''
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

    cursor.execute('''
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

    conn.commit()


def get_team_id(team_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT team_id FROM teams WHERE team_name = ?
    ''', (team_name,))

    result = cursor.fetchone()

    return result[0]


def generate_schedule(year, month, current_team):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    shift_circle = [1, 2, 3, 3]
    team_position = get_team_id(current_team)

    _, days_in_month = monthrange(year, month)

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)

        for shift in shift_circle:
            if team_position > 4:
                team_position = 1

            team_id = team_position
            shift_type_id = shift

            cursor.execute('''
                INSERT INTO schedule (team_id, shift_type_id, date)
                VALUES (?, ?, ?)
            ''', (team_id, shift_type_id, current_date))

            team_position += 1

        shift_circle.append(shift_circle.pop(0))

    conn.commit()


def show_schedule():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.date, st.name, t.team_name 
        FROM
            schedule as s 
        JOIN 
            shift_types as st
        ON
            st.shift_type_id = s.shift_type_id
        JOIN 
            teams as t 
        ON 
            t.team_id = s.team_id
    ''')

    result = cursor.fetchall()
    return result


# def print_result():
#     result = show_schedule()
#     grouped_schedule = {}
#
#     for item in result:
#         shift_date, shift_type, team = item
#
#         if shift_date not in grouped_schedule:
#             grouped_schedule[shift_date] = []
#         grouped_schedule[shift_date].append([shift_type, team])
#
#     return grouped_schedule
#
# for key, value in print_result().items():
#     team = ''
#     shift = ''
#     print('Дата       |------Смяна----|')
#     for item in value:
#         shift += item[0]
#         team += item[1]
#
#     team = ' | '.join(list(team))
#     shift = ' | '.join(list(shift))
#     weekday = datetime.strptime(key, '%Y-%m-%d').date().strftime('%A')
#
#     print(f'{weekday} | {team} | \n{key} | {shift} |')

def fetch_dates():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date FROM schedule WHERE '2024-01-01' <= date AND date <= '2024-12-31' GROUP BY date
    ''')

    result = cursor.fetchall()
    return result
