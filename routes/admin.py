from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.database import get_db_connection

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/dashboard')
def admin_dashboard():
    """Render Admin Dashboard with Right Pane Options"""
    if 'role' not in session or session['role'] != 'Admin':
        return redirect(url_for('auth.login'))
    return render_template('admin_dashboard.html')

@admin_blueprint.route('/get_filters', methods=['GET'])
def get_filters():
    """Fetch unique department names and states for filtering"""
    if 'role' not in session or session['role'] != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch department names
    cursor.execute("SELECT dep_name FROM payroll.department;")
    departments = [row[0] for row in cursor.fetchall()]

    # Fetch state names
    cursor.execute("SELECT DISTINCT state FROM payroll.employee;")
    states = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify({"departments": departments, "states": states})

@admin_blueprint.route('/employees', methods=['GET'])
def get_all_employees():
    """Fetch all employees for Admin View"""
    if 'role' not in session or session['role'] != 'Admin':
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

@admin_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Fetch all users from the database"""
    if 'role' not in session or session['role'] != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT e.e_id, e.e_name, u.user_id, u.username, r.role_name, u.role_id 
        FROM payroll.users u
        JOIN payroll.roles r ON r.role_id = u.role_id
        LEFT JOIN payroll.employee e ON e.e_id = u.employee_id;
    """
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([
        {"Employee_id": row[0], "Employee_name": row[1], "user_id": row[2], "user_name": row[3],
         "Role_name": row[4], "role_id": row[5]}
        for row in users
    ])

@admin_blueprint.route('/roles_dropdown', methods=['GET'])
def roles_dropdown():
    """Fetch dynamic role options for dropdown"""
    if 'role' not in session or session['role'] != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role_id, role_name FROM payroll.roles;")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{"role_id": row[0], "role_name": row[1]} for row in roles])

@admin_blueprint.route('/update_role', methods=['POST'])
def update_role():
    """Update the role_id of a user given their employee_id"""
    if 'role' not in session or session['role'] != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    employee_id = data.get("employee_id")
    role_id = data.get("role_id")

    if not employee_id or not role_id:
        return jsonify({"error": "Invalid input"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE payroll.users SET role_id = %s WHERE employee_id = %s"
        cursor.execute(query, (role_id, employee_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": "Role updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_blueprint.route('/roles', methods=['GET'])
def get_all_roles():
    """Fetch all rolesfor Admin View"""
    if 'role' not in session or session['role'] != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role_id, role_name FROM payroll.roles;")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    print(roles)
    return jsonify([{"Role_ID": row[0], "Role_Name": row[1]} for row in roles])