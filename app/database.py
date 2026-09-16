import sqlite3

DATABASE_NAME = "equipment_rental.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            total_quantity INTEGER NOT NULL CHECK(total_quantity > 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            borrower_id INTEGER NOT NULL,
            equipment_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            deposit REAL NOT NULL CHECK(deposit >= 0),
            late_fee REAL DEFAULT 0,
            refund_amount REAL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'ACTIVE',

            FOREIGN KEY (borrower_id) REFERENCES borrowers(id),
            FOREIGN KEY (equipment_id) REFERENCES equipment(id)
        )
    """)

    connection.commit()
    connection.close()
def seed_data():
    connection = get_connection()
    cursor = connection.cursor()

    equipment = [
        ("DSLR Camera", "Camera", 3),
        ("Projector", "Display", 2),
        ("Microphone", "Audio", 5),
        ("Tripod", "Camera Support", 4)
    ]

    cursor.executemany("""
        INSERT INTO equipment (name, category, total_quantity)
        VALUES (?, ?, ?)
    """, equipment)

    connection.commit()
    connection.close()