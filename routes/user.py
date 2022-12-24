from flask import Blueprint, render_template

from models.auth.auth_functions import customer_login_required, restricted_customer_error, staff_login_required, \
    restricted_staff_error

user = Blueprint('user', __name__)


@user.route('/CustomerDashboard')
def customer_dashboard():
    if customer_login_required():
        return render_template('user/customer_dashboard.html')
    else:
        return restricted_customer_error()


@user.route('/StaffDashboard')
def staff_dashboard():
    if staff_login_required():
        return render_template('user/staff_dashboard.html')
    else:
        return restricted_staff_error()


@user.route('/customerProfile')
def customer_profile():
    if customer_login_required():
        return render_template('user/customer_profile.html')
    else:
        return restricted_customer_error()


@user.route('/StaffProfile')
def staff_profile():
    if staff_login_required():
        return render_template('user/staff_profile.html')
    else:
        return restricted_staff_error()
