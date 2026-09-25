import flask
from flask_cors import CORS
import sqlite3
import random

app = flask.Flask(__name__)
CORS(app)

# Temporary memory to store the real OTPs
otp_store = {}
# New temporary memory for Student Wallet PINs
pin_store = {}

@app.route('/api/student/generate-pin/<student_id>', methods=['GET'])
def generate_pin(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    conn.close()

    if not student:
        return flask.jsonify({"success": False, "message": "Student ID not found"}), 404
    
    # Generate a 6-digit PIN and store it linked to the student ID
    real_pin = str(random.randint(100000, 999999))
    pin_store[real_pin] = student_id
    
    print(f"🔐 [SSI WALLET] Generated Access PIN {real_pin} for {student_id}")
    return flask.jsonify({"success": True, "pin": real_pin})

@app.route('/api/officer/verify-pin/<pin>', methods=['GET'])
def officer_verify_pin(pin):
    # Check if the PIN exists in active memory
    student_id = pin_store.get(pin)
    
    if not student_id:
        return flask.jsonify({"success": False, "message": "Invalid or Expired PIN"}), 401

    conn = get_db_connection()
    # 1. Fetch Core Identity
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    
    if student:
        # 2. Fetch all dynamic credentials for this student
        ledger_records = conn.execute(
            'SELECT issuer_name, credential_name, credential_value FROM credentials_ledger WHERE student_id = ?', 
            (student_id,)
        ).fetchall()
        
        conn.close()
        
        # Burn the PIN so it can never be used again
        del pin_store[pin] 
        
        # 3. Stitch them together into one JSON package
        student_data = dict(student)
        student_data['credentials'] = [dict(record) for record in ledger_records]
        
        return flask.jsonify({"success": True, "data": student_data})
    else:
        conn.close()
        return flask.jsonify({"success": False, "message": "Database Error"}), 500

# THE MISSING FUNCTION: Tells Flask how to open the vault
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/request-consent/<student_id>', methods=['GET'])
def request_otp(student_id):
    conn = get_db_connection()
    # Fetch both contact methods
    student = conn.execute('SELECT phone_number, email_id FROM students WHERE student_id = ?', (student_id,)).fetchone()
    conn.close()

    if student is None:
        return flask.jsonify({"success": False, "message": "Student ID not found"}), 404
    
    phone = student['phone_number']
    email = student['email_id']
    
    real_otp = str(random.randint(1000, 9999))
    otp_store[student_id] = real_otp
    
    # SIMULATE SMS & EMAIL GATEWAYS in the terminal
    print(f"\n📱 [SMS GATEWAY] Sending OTP {real_otp} to {phone}")
    print(f"📧 [EMAIL GATEWAY] Sending OTP {real_otp} to {email}\n")

    # Mask the details for the frontend UI
    masked_phone = f"******{phone[-4:]}"
    email_parts = email.split("@")
    masked_email = f"{email_parts[0][0]}***@{email_parts[1]}"
    
    return flask.jsonify({
        "success": True, 
        "masked_phone": masked_phone,
        "masked_email": masked_email
    })

@app.route('/api/verify/<student_id>', methods=['GET'])
def get_student(student_id):
    user_otp = flask.request.args.get('otp')
    
    if not user_otp or otp_store.get(student_id) != user_otp:
        return flask.jsonify({"success": False, "message": "Invalid OTP. Consent Denied."}), 401

    conn = get_db_connection()
    # 1. Fetch Core Identity
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()

    if student:
        # 2. Fetch all dynamic credentials for this student
        ledger_records = conn.execute(
            'SELECT issuer_name, credential_name, credential_value FROM credentials_ledger WHERE student_id = ?', 
            (student_id,)
        ).fetchall()
        
        conn.close()
        
        # Clear the OTP so it can't be reused
        del otp_store[student_id]
        
        # 3. Stitch them together into one JSON package
        student_data = dict(student)
        student_data['credentials'] = [dict(record) for record in ledger_records]
        
        return flask.jsonify({"success": True, "data": student_data})
    else:
        conn.close()
        return flask.jsonify({"success": False, "message": "Student ID not found"}), 404
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)