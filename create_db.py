import sqlite3

def create_database():
    conn = sqlite3.connect('C:/Users/user/Desktop/test.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Создание таблицы пациентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Создание таблицы организаций
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Создание таблицы категорий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Создание таблицы действий
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')

    # Создание таблицы наблюдений
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        position TEXT NOT NULL,
        organization_id INTEGER,
        start_time TEXT NOT NULL,
        end_time TEXT,
        duration INTEGER,
        comment TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (organization_id) REFERENCES organizations (id)
    )
    ''')

    # Создание таблицы завершенных осмотров
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS completed_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        position TEXT NOT NULL,
        organization_id INTEGER,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        total_time INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (organization_id) REFERENCES organizations (id)
    )
    ''')

    # Добавление администратора
    cursor.execute('''
    INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
