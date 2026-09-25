import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# 1. Clear old tables to start fresh
cursor.execute('DROP TABLE IF EXISTS credentials_ledger')
cursor.execute('DROP TABLE IF EXISTS students')

# 2. Table 1: Core Identity (Agnostic to exams)
cursor.execute('''
    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        full_name TEXT,
        dob TEXT,
        father_name TEXT,
        mother_name TEXT,
        aadhaar_number TEXT,
        category TEXT,
        phone_number TEXT,
        email_id TEXT,
        profile_pic TEXT 
    )
''')

# 3. Table 2: The Dynamic Credential Ledger
cursor.execute('''
    CREATE TABLE credentials_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        issuer_name TEXT,
        credential_name TEXT,
        credential_value TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
''')

# 4. Insert Core Identity Data
sample_students = [
    ("APAAR1001", "Yashas H N", "2008-02-29", "Nagaraju H G", "Pushpa H P", "XXXX-XXXX-1001", "General", "6362848869", "yashashn45@gmail.com", "/static/student1.jpg"),
]
cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_students)

# 5. Insert Dynamic Credentials for APAAR1001
sample_credentials = [
    # (student_id, issuer_name, credential_name, credential_value)
    ("APAAR1001", "CBSE", "10th Board Score", "98.2%"),
    ("APAAR1001", "Karnataka Dept of Pre-University Education", "12th Board Score", "97.67%"),
    ("APAAR1001", "National Testing Agency (NTA)", "JEE Mains Percentile", "99.559"),
    ("APAAR1001", "IIT Joint Admission Board", "JEE Advanced Rank", "2611")
]
cursor.executemany("INSERT INTO credentials_ledger (student_id, issuer_name, credential_name, credential_value) VALUES (?, ?, ?, ?)", sample_credentials)

conn.commit()
conn.close()

print("Enterprise Vault rebuilt with Dynamic Ledger!")