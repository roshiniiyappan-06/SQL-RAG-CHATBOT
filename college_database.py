import sqlite3

conn = sqlite3.connect("college.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    cgpa REAL
)
""")

students = [
    (1, "Rose", "CSE", 8.9),
    (2, "Anu", "ECE", 8.5),
    (3, "Rahul", "IT", 9.1),
    (4, "Priya", "CSE", 9.3),
    (5, "Kiran", "EEE", 8.2)
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", students)

conn.commit()
conn.close()

print("Database Created Successfully!")