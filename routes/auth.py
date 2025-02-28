from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.database import get_db_connection

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login. Must be preceded by a dashboard selection from the landing page."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        # Retrieve user info
        cursor.execute(
            "SELECT user_id, username, password_hash, role_id, employee_id FROM payroll.users WHERE username = %s", 
            (username,)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user[2], password):  # user[2] is the stored password_hash
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['employee_id'] = user[4]

            # Retrieve role name from roles table
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT role_name FROM payroll.roles WHERE role_id = %s", (user[3],))
            role = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            session['role'] = role

            flash(f"Welcome, {username}!", "success")
            print(f"DEBUG: Login Successful | User: {session['username']} | Role: {session['role']} | Requested Dashboard: {session['requested_dashboard']}")
            return redirect(url_for('dashboard'))
        
        flash("Invalid username or password", "danger")

    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    """Handles user logout"""
    session.clear()
    flash("You have been logged out", "info")
    return render_template('landing.html')

@auth_blueprint.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Allows users to change their passwords"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("New passwords do not match", "danger")
            return redirect(url_for('auth.change_password'))

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM payroll.users WHERE user_id = %s", (session['user_id'],))
        stored_password = cursor.fetchone()[0]

        if not check_password_hash(stored_password, old_password):
            flash("Old password is incorrect", "danger")
            return redirect(url_for('auth.change_password'))

        # Hash new password before storing
        from werkzeug.security import generate_password_hash
        new_password_hash = generate_password_hash(new_password)

        cursor.execute("UPDATE payroll.users SET password_hash = %s WHERE user_id = %s", (new_password_hash, session['user_id']))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Password changed successfully!", "success")
        return redirect(url_for('auth.login'))

    return render_template('change_password.html')
