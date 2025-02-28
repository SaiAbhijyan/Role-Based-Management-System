from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for,flash
import pandas as pd
import io
from flask import Response
from models.database import get_db_connection

from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify


manager_blueprint = Blueprint('manager', __name__, url_prefix='/manager')

@manager_blueprint.route('/dashboard')
def manager_dashboard():
    """Render Manager Dashboard."""
    if 'role' not in session or session['role'] != 'Manager':
        return redirect(url_for('auth.login'))

    return render_template('manager_dashboard.html')


@manager_blueprint.route('/get_filters', methods=['GET'])
def get_filters():
    """Fetch unique department names and states for filtering"""
    if 'role' not in session or session['role'] != 'Manager':
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch department names
    cursor.execute("SELECT dep_name FROM payroll.department;")
    departments = [row[0] for row in cursor.fetchall()]

    # Fetch state names
    cursor.execute("SELECT DISTINCT state FROM payroll.tax_deductions;")
    states = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify({"departments": departments, "states": states})

@manager_blueprint.route('/employees', methods=['GET'])
def get_employees():
    """Fetch employees based on department, state, or name search."""
    if 'role' not in session or session['role'] != 'Manager':
        return jsonify({"error": "Unauthorized"}), 403

    department = request.args.get('department', None)
    state = request.args.get('state', None)
    search_name = request.args.get('search_name', None)

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT e.E_id, e.E_name, e.Designation, d.dep_name, d.dep_id
        FROM payroll.Employee e
        JOIN payroll.Department d ON e.dep_id = d.dep_id
        WHERE 1=1
    """
    params = []

    if department:
        query += " AND d.dep_name = %s"
        params.append(department)

    if state:
        query += " AND e.state = %s"
        params.append(state)

    if search_name:
        query += " AND e.E_name ILIKE %s"
        params.append(f"%{search_name}%")

    cursor.execute(query, tuple(params))
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify([
        {"E_id": row[0], "E_name": row[1], "Designation": row[2], "Department": row[3], "Department_ID": row[4]}
        for row in employees
    ])

