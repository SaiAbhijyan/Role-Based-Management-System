from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.database import get_db_connection

HR_blueprint = Blueprint('HR', __name__, url_prefix='/HR')

@HR_blueprint.route('/dashboard')
def HR_dashboard():
    if 'role' not in session or session['role'] != 'HR':
        return redirect(url_for('auth.login'))
    return render_template('HR_dashboard.html')

@HR_blueprint.route('/employees', methods=['GET'])
def get_all_employees():
    if 'role' not in session or session['role'] != 'HR':
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT e.e_id, e.e_name, e.designation, e.salary, e.bonus, e.state, e.zip_code, d.dep_name 
        FROM payroll.employee e
        JOIN payroll.department d ON e.dep_id = d.dep_id;
    """
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([
        {"E_id": row[0], "E_name": row[1], "Designation": row[2], "Salary": row[3],
         "Bonus": row[4], "State": row[5], "Zip_Code": row[6], "Department": row[7]}
        for row in employees
    ])

@HR_blueprint.route('/departments', methods=['GET'])
def get_departments():
    if 'role' not in session or session['role'] != 'HR':
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dep_id FROM payroll.department;")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"dep_id": row[0]} for row in departments])

@HR_blueprint.route('/add_employee', methods=['POST'])
def add_employee():
    if 'role' not in session or session['role'] != 'HR':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    required_fields = ['employee_name', 'designation', 'salary', 'bonus', 'state', 'zip_code', 'dep_id']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "All fields are required."}), 400

    employee_name = data['employee_name'].strip()
    designation = data['designation'].strip()
    salary = data['salary']
    bonus = data['bonus']
    state = data['state'].strip()
    zip_code = data['zip_code'].strip()
    dep_id = data['dep_id']

    if len(zip_code) != 5 or not zip_code.isdigit():
        return jsonify({"error": "Zip Code must be exactly 5 digits."}), 400
    if not employee_name or not designation:
        return jsonify({"error": "Employee Name and Designation cannot be empty."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    duplicate_query = """
        SELECT * FROM payroll.employee
        WHERE e_name = %s AND designation = %s AND salary = %s AND bonus = %s AND state = %s AND zip_code = %s AND dep_id = %s;
    """
    cursor.execute(duplicate_query, (employee_name, designation, salary, bonus, state, zip_code, dep_id))
    duplicate = cursor.fetchone()
    if duplicate:
        cursor.close()
        conn.close()
        return jsonify({"error": "Duplicate employee record found."}), 400

    try:
        insert_query = """
            INSERT INTO payroll.employee (e_name, designation, salary, bonus, state, zip_code, dep_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (employee_name, designation, salary, bonus, state, zip_code, dep_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": "Employee added successfully."}), 200
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@HR_blueprint.route('/filter_states', methods=['GET'])
def filter_states():
    if 'role' not in session or session['role'] != 'HR':
        return jsonify({"error": "Unauthorized"}), 403
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT state FROM payroll.tax_deductions;")
    states = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"state": row[0]} for row in states])

@HR_blueprint.route('/filter_employees', methods=['POST'])
def filter_employees():
    if 'role' not in session or session['role'] != 'HR':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    filter_name = data.get('employee_name', '').strip()
    filter_state = data.get('state', '').strip()
    filter_dep = data.get('dep_id', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT e.e_id, e.e_name, e.designation, e.salary, e.bonus, e.state, e.zip_code, d.dep_name 
        FROM payroll.employee e
        JOIN payroll.department d ON e.dep_id = d.dep_id
        WHERE 1=1
    """
    params = []
    if filter_name:
        query += " AND e.e_name ILIKE %s"
        params.append(f"%{filter_name}%")
    if filter_state:
        query += " AND e.state = %s"
        params.append(filter_state)
    if filter_dep:
        query += " AND e.dep_id = %s"
        params.append(filter_dep)
    
    cursor.execute(query, tuple(params))
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([
        {"E_id": row[0], "E_name": row[1], "Designation": row[2], "Salary": row[3],
         "Bonus": row[4], "State": row[5], "Zip_Code": row[6], "Department": row[7]}
        for row in employees
    ])

@HR_blueprint.route('/update_employee', methods=['POST'])
def update_employee():
    if 'role' not in session or session['role'] != 'HR':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    employee_id = data.get('employee_id')
    updated_data = data.get('updated_data')
    if not employee_id or not updated_data:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT e_name, designation, salary, bonus, state, zip_code, dep_id FROM payroll.employee WHERE e_id = %s", (employee_id,))
    current = cursor.fetchone()
    if not current:
        cursor.close()
        conn.close()
        return jsonify({"error": "Employee not found"}), 404

    current_data = {
        "employee_name": current[0],
        "designation": current[1],
        "salary": str(current[2]),
        "bonus": str(current[3]),
        "state": current[4],
        "zip_code": current[5],
        "dep_id": str(current[6])
    }

    # Determine fields to update, skipping any empty new value
    fields_to_update = {}
    for key, new_val in updated_data.items():
        # Skip update if new value is empty
        if new_val == "" or new_val is None:
            continue
        # For numeric fields and dep_id, compare as string
        if key in ["salary", "bonus", "dep_id"]:
            new_val = str(new_val)
        if str(new_val) != str(current_data.get(key, '')):
            fields_to_update[key] = new_val

    if not fields_to_update:
        cursor.close()
        conn.close()
        return jsonify({"success": "No changes made."}), 200

    mapping = {
        "employee_name": "e_name",
        "designation": "designation",
        "salary": "salary",
        "bonus": "bonus",
        "state": "state",
        "zip_code": "zip_code",
        "dep_id": "dep_id"
    }
    set_clause = ", ".join(f"{mapping[k]} = %s" for k in fields_to_update)
    values = list(fields_to_update.values())
    values.append(employee_id)
    
    update_query = f"UPDATE payroll.employee SET {set_clause} WHERE e_id = %s"
    try:
        cursor.execute(update_query, tuple(values))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": "Employee updated successfully."}), 200
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500
