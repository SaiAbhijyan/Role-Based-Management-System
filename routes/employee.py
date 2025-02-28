from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from models.database import get_db_connection
from flask import jsonify

employee_blueprint = Blueprint('employee', __name__, url_prefix='/employee')


@employee_blueprint.route('/dashboard')
def employee_dashboard():
    if 'role' not in session :
        return redirect(url_for('auth.login'))
    return render_template('employee_dashboard.html')

@employee_blueprint.route('/details',methods=['GET'])
def view_employee_details():
    """Fetch personal details for logged-in employee"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if 'employee_id' not in session:
        return redirect(url_for('auth.login'))

    employee_id = session['employee_id']
    print(f"🔍 Debug: Employee ID from session → {employee_id}")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    WITH salary_bracket AS (
        SELECT E_id,
            CASE
                WHEN salary BETWEEN 0 AND 11600 THEN (salary * 0.10)
                WHEN salary BETWEEN 11601 AND 47150 THEN (salary * 0.12)
                WHEN salary BETWEEN 47151 AND 100525 THEN (salary * 0.22)
                WHEN salary BETWEEN 100526 AND 191950 THEN (salary * 0.24)
                WHEN salary BETWEEN 191951 AND 243725 THEN (salary * 0.32)
                WHEN salary BETWEEN 243726 AND 609350 THEN (salary * 0.35)
                WHEN salary > 609351  THEN (salary * 0.37)
            END AS Federal_deducation
        FROM payroll.employee
    )
    SELECT e.E_id, e.E_name, e.Designation, d.dep_name, e.Salary AS Gross_salary, 
           (Federal_deducation + (e.salary * td.state_tax / 100) + (e.salary * 0.0765)) AS Deductable,
           (e.salary - ((Federal_deducation + (e.salary * td.state_tax / 100) + (e.salary * 0.0765))) + e.Bonus) AS Net_Salary
    FROM payroll.Employee e
    JOIN payroll.Department d ON e.dep_id = d.dep_id
    JOIN payroll.tax_deductions td ON e.State = td.state 
    JOIN salary_bracket sb ON e.E_id = sb.E_id
    WHERE e.E_id = %s;
    """

    cursor.execute(query, (employee_id,))
    employee_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not employee_data:
        flash("No employee data found!", "danger")
        return redirect(url_for('dashboard'))
 

    return jsonify(
        {
            "E_id": employee_data[0], "E_name": employee_data[1], "Designation": employee_data[2], "Department": employee_data[3], "Gross_salary": employee_data[4],
         "Deductable": employee_data[5],"Net_Salary": employee_data[6]}
    )

