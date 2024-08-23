import sqlite3
from typing import List, Tuple, Any, Dict
from datetime import date
from MainWindowSingleton import *

def InitializingDatabase():
    conn = sqlite3.connect('Task.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User';")
    userTableExists = cursor.fetchone()

    if not userTableExists:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            userID INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            birthdate DATE,
            lastLogin DATE,
            isReminder INTEGER,
            intervalHour INTEGER
        );
        ''')
        conn.commit()
        
        CreateRecord('User', {'username': "User", 'password': hashingString("User"), 'birthdate': hashingString("2004-03-15"), 'lastLogin': None, 'isReminder': 1, 'intervalHour': 3})
        CreateRecord('User', {'username': "Admin", 'password': hashingString("Admin"), 'birthdate': hashingString("2000-01-01"), 'lastLogin': None, 'isReminder': 1, 'intervalHour': 3})

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Companion';")
    companionTableExists = cursor.fetchone()

    if not companionTableExists:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companion (
            companionID INTEGER PRIMARY KEY,
            userID INTEGER,
            level INTEGER,
            friendshipPoint INTEGER,
            friendshipPointNext INTEGER,
            friendshipPointMultiplier INTEGER,
            FOREIGN KEY (userID) REFERENCES User (userID) ON DELETE CASCADE
        );
        ''')
        conn.commit()
        
        CreateRecord('Companion', {'userID': 1, 'level': 1, 'friendshipPoint': 0, 'friendshipPointNext': 10, 'friendshipPointMultiplier': 1})
        CreateRecord('Companion', {'userID': 2, 'level': 1, 'friendshipPoint': 0, 'friendshipPointNext': 10, 'friendshipPointMultiplier': 1})
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Custom_Task';")
    customTaskTableExists = cursor.fetchone()

    if not customTaskTableExists:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Custom_Task (
            customTaskID INTEGER PRIMARY KEY,
            userID INTEGER,
            title TEXT,
            note TEXT,
            difficulty TEXT,
            dueDate DATE,
            createdDate DATE,
            FOREIGN KEY (userID) REFERENCES User (userID) ON DELETE CASCADE
        );
        ''')
        conn.commit()
        
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 1", 'note': "Note 1", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 2", 'note': "Note 2", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 3", 'note': "Note 3", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 4", 'note': "Note 4", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 5", 'note': "Note 5", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 6", 'note': "Note 6", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 7", 'note': "Note 7", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 8", 'note': "Note 8", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 9", 'note': "Note 9", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 10", 'note': "Note 10", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 11", 'note': "Note 11", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 12", 'note': "Note 12", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 13", 'note': "Note 13", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 14", 'note': "Note 14", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 15", 'note': "Note 15", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 16", 'note': "Note 16", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 17", 'note': "Note 17", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 18", 'note': "Note 18", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 19", 'note': "Note 19", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 20", 'note': "Note 20", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 21", 'note': "Note 21", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 22", 'note': "Note 22", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 23", 'note': "Note 23", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 24", 'note': "Note 24", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 25", 'note': "Note 25", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 26", 'note': "Note 26", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 27", 'note': "Note 27", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 28", 'note': "Note 28", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 29", 'note': "Note 29", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 30", 'note': "Note 30", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 31", 'note': "Note 31", 'difficulty': "Easy", 'dueDate': "2024-10-09", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 32", 'note': "Note 32", 'difficulty': "Medium", 'dueDate': "2024-11-11", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 33", 'note': "Note 33", 'difficulty': "Hard", 'dueDate': "2024-12-25", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 34", 'note': "Note 34", 'difficulty': "Extreme", 'dueDate': "2025-01-01", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 35", 'note': "Note 35", 'difficulty': "Easy", 'dueDate': "2025-02-02", 'createdDate': date.today()})
        
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 36", 'note': "Note 36", 'difficulty': "Easy", 'dueDate': "2023-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 37", 'note': "Note 37", 'difficulty': "Easy", 'dueDate': "2023-02-02", 'createdDate': date.today()})
        # CreateRecord('Custom_Task', {'userID': 1, 'title': "Custom Task 38", 'note': "Note 38", 'difficulty': "Easy", 'dueDate': date.today(), 'createdDate': date.today()})
        
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Completed_Custom_Task';")
    completedCustomTaskTableExists = cursor.fetchone()

    if not completedCustomTaskTableExists:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Completed_Custom_Task (
            completedCustomTaskID INTEGER PRIMARY KEY,
            customTaskID INTEGER,
            completedDate DATE,
            isOverdue INTEGER,
            FOREIGN KEY (customTaskID) REFERENCES Custom_Task (customTaskID) ON DELETE CASCADE
        );
        ''')
        conn.commit()
        
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Daily_Task';")
    dailyTaskTableExists = cursor.fetchone()

    if not dailyTaskTableExists:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Daily_Task (
            dailyTaskID INTEGER PRIMARY KEY,
            userID INTEGER,
            title TEXT,
            note TEXT,
            difficulty TEXT,
            createdDate DATE,
            FOREIGN KEY (userID) REFERENCES User (userID) ON DELETE CASCADE
        );
        ''')
        conn.commit()
        
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 1", 'note': "Daily Note 1", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 2", 'note': "Daily Note 2", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 3", 'note': "Daily Note 3", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 4", 'note': "Daily Note 4", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 5", 'note': "Daily Note 5", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 6", 'note': "Daily Note 6", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 7", 'note': "Daily Note 7", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 8", 'note': "Daily Note 8", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 9", 'note': "Daily Note 9", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 10", 'note': "Daily Note 10", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 11", 'note': "Daily Note 11", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 12", 'note': "Daily Note 12", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 13", 'note': "Daily Note 13", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 14", 'note': "Daily Note 14", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 15", 'note': "Daily Note 15", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 16", 'note': "Daily Note 16", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 17", 'note': "Daily Note 17", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 18", 'note': "Daily Note 18", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 19", 'note': "Daily Note 19", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 20", 'note': "Daily Note 20", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 21", 'note': "Daily Note 21", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 22", 'note': "Daily Note 22", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 23", 'note': "Daily Note 23", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 24", 'note': "Daily Note 24", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 25", 'note': "Daily Note 25", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 26", 'note': "Daily Note 26", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 27", 'note': "Daily Note 27", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 28", 'note': "Daily Note 28", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 29", 'note': "Daily Note 29", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 30", 'note': "Daily Note 30", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 31", 'note': "Daily Note 31", 'difficulty': "Easy", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 32", 'note': "Daily Note 32", 'difficulty': "Medium", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 33", 'note': "Daily Note 33", 'difficulty': "Hard", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 34", 'note': "Daily Note 34", 'difficulty': "Extreme", 'createdDate': date.today()})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 35", 'note': "Daily Note 35", 'difficulty': "Easy", 'createdDate': date.today()})
        
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 36", 'note': "Daily Note 36", 'difficulty': "Easy", 'createdDate': "2023-02-02"})
        # CreateRecord('Daily_Task', {'userID': 1, 'title': "Daily Task 37", 'note': "Daily Note 37", 'difficulty': "Easy", 'createdDate': "2023-02-02"})
        
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Completed_Daily_Task';")
    completedDailyTaskTableExists = cursor.fetchone()

    if not completedDailyTaskTableExists:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Completed_Daily_Task (
            completedDailyTaskID INTEGER PRIMARY KEY,
            dailyTaskID INTEGER,
            completedDate DATE,
            isOverdue INTEGER,
            FOREIGN KEY (dailyTaskID) REFERENCES Daily_Task (dailyTaskID) ON DELETE CASCADE
        );
        ''')
        conn.commit()

    conn.close()
    
def CreateRecord(table_name: str, data: Dict[str, Any]) -> None:
    conn = sqlite3.connect('Task.db')
    cursor = conn.cursor()

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)

    conn.commit()
    conn.close()
    
# CreateRecord('Custom_Task', {'userID': 1, 'title': entry_1.get(), 'note': entry_2.get(), 'difficulty': selectedOption1.get(), 'dueDate': selectedDate})
    
def FetchRecord(table_name: str, columns: List[str] = None, where_clause: str = None, params: Tuple[Any, ...] = ()) -> List[Tuple]:
    conn = sqlite3.connect('Task.db')
    cursor = conn.cursor()

    if columns:
        columns_str = ', '.join(columns)
    else:
        columns_str = '*'

    query = f"SELECT {columns_str} FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return rows

# FetchRecord('User', columns=['userID', 'username', 'isAutoStart', 'isReminder', 'intervalHour'], where_clause='userID = ?', params=(1,))
# FetchRecord('User', columns=['password'], where_clause="username = ? AND birthdate = ?", params=(username, hashedBirthdate,))

def UpdateRecord(table_name: str, data: Dict[str, Any], where_clause: str, params: Tuple[Any, ...]) -> None:
    conn = sqlite3.connect('Task.db')
    cursor = conn.cursor()

    set_clause = ', '.join([f"{col} = ?" for col in data.keys()])
    values = tuple(data.values()) + params

    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    cursor.execute(query, values)

    conn.commit()
    conn.close()
    
# UpdateRecord('Companion',  {'level': level, 'friendshipPoint': friendshipPoint, 'friendshipPointNext': friendshipPointNext}, 'companionID = ?', (companionID,))
    
def DeleteRecord(table_name: str, where_clause: str, params: Tuple[Any, ...]) -> None:
    conn = sqlite3.connect('Task.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    cursor.execute(query, params)

    conn.commit()
    conn.close()
    
# DeleteRecord('Custom_Task', 'customTaskID = ?', (customTaskID,))