import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS students')

# Added email_id TEXT at the end
cursor.execute('''
    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        full_name TEXT,
        dob TEXT,
        father_name TEXT,
        mother_name TEXT,
        aadhaar_number TEXT,
        category TEXT,
        board_name TEXT,
        board_score REAL,
        jee_adv_rank INTEGER,
        phone_number TEXT,
        email_id TEXT,
        profile_pic TEXT
    )
''')

# Added dummy emails as the 12th item in each tuple
sample_students = [
    ("APAAR1001", "Yashas H N", "2008-02-29", "Nagaraju H G", "Pushpa H P", "XXXX-XXXX-1001", "General", "Karnataka 2nd PUC", 97.67, 2611, "6362848869", "yashashn45@gmail.com", "/static/APAAR1001.jpg"),
    ("APAAR1002", "Diya Rao", "2007-11-20", "Sanjay Rao", "Meena Rao", "XXXX-XXXX-1002", "OBC-NCL", "CBSE Class 12", 94.20, 1500, "9876543210", "diya@example.com", "/static/APAAR1002.jpg"),
    ("APAAR1011", "Kiran Kumar", "2008-04-12", "Rajesh拾 Kumar", "Lakshmi Kumar", "XXXX-XXXX-1011", "OBC", "CBSE", 94.50, 4521, "9876543210", "kiran@example.com", "/static/APAAR1011.jpg"),
    ("APAAR1012", "Sneha Sharma", "2007-09-25", "Amit Sharma", "Priya Sharma", "XXXX-XXXX-1012", "General", "ICSE", 98.20, 1205, "9876543210", "sneha@example.com", "/static/APAAR1012.jpg"),
    ("APAAR1013", "Arjun Reddy", "2008-01-14", "Prakash Reddy", "Kavitha Reddy", "XXXX-XXXX-1013", "General", "Telangana State Board", 96.80, 3110, "9876543210", "arjun@example.com", "/static/APAAR1013.jpg"),
    ("APAAR1014", "Pooja Patil", "2007-11-03", "Sunil Patil", "Anita Patil", "XXXX-XXXX-1014", "SC", "Maharashtra HSC", 89.40, 15302, "9876543210", "pooja@example.com", "/static/APAAR1014.jpg"),
    ("APAAR1015", "Rohan Gupta", "2008-06-22", "Vijay Gupta", "Meena Gupta", "XXXX-XXXX-1015", "General", "CBSE", 92.10, 8433, "9876543210", "rohan@example.com", "/static/APAAR1015.jpg")
]

# We now use 12 question marks for the 12 columns
cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_students)

conn.commit()
conn.close()

print("Vault rebuilt with Phone Numbers and Email IDs!")