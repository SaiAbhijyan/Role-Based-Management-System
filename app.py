
from flask import Flask, render_template, redirect, url_for, session, flash
from routes.auth import auth_blueprint
from routes.employee import employee_blueprint
from routes.manager import manager_blueprint
from routes.admin import admin_blueprint
from routes.HR import HR_blueprint
from models.database import get_db_connection
from datetime import timedelta  #---> "This is for session timeout example"

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'  #This is for server side storage of session data 
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

# Register Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(employee_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(manager_blueprint)
app.register_blueprint(HR_blueprint)

@app.route('/')
def landing():
    """General landing page with dashboard options"""
    return render_template('landing.html')

@app.route('/choose/<dashboard>')
def choose_dashboard(dashboard):
    """Store chosen dashboard in session and redirect to login"""
    if dashboard not in ['Employee', 'Manager', 'Admin','HR']:
        flash("Invalid dashboard selection", "danger")
        return redirect(url_for('landing'))
    # Store the requested dashboard in a uniform format
    session['requested_dashboard'] = dashboard  # "Personal", "Manager", "Admin" or "HR"
    print(f"The dashboard you choose: {session['requested_dashboard']}")
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    """Redirect users to their chosen dashboard after login"""
    if 'role' not in session or 'requested_dashboard' not in session:
        flash("Please choose a dashboard from the landing page.", "warning")
        return redirect(url_for('landing'))
    requested = session['requested_dashboard'] # 
    user_role = session['role']  # Example: "Manager"
    if requested == 'Employee':
        # All employees (including Managers and Admins) should be able to access their own personal dashboard
        return redirect(url_for('employee.employee_dashboard'))
    elif requested == 'Manager':
        if user_role == 'Manager':
            return redirect(url_for('manager.manager_dashboard'))
        else:
            flash("Access denied: Only Managers can access the Manager Dashboard.", "danger")
            return redirect(url_for('landing'))
    elif requested == 'Admin':
        if user_role == 'Admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash("Access denied: Only Admins can access the Admin Dashboard.", "danger")
            return redirect(url_for('landing'))
    elif requested == 'HR':
        if user_role == 'HR':
            return redirect(url_for('HR.HR_dashboard'))  
        else:
            flash("Access denied: Only Admins can access the Admin Dashboard.", "danger")
            return redirect(url_for('landing'))
    else:
        flash("Invalid dashboard selection.", "danger")
        return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
