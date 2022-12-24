from flask import Blueprint, render_template, request, session, flash
from models.auth.auth_forms import LoginForm, RegisterForm
from models.auth.auth_functions import *
from models.auth.account_classes import Customer

auth = Blueprint('auth', __name__)


@auth.route('/CustomerRegister', methods=["POST", "GET"])
def customer_register():
    error_messages = []
    register_form = RegisterForm()
    if not validate_username(register_form.username.data, relative_path_to_db='DB'):
        error_messages.append("Username is already taken, please use another one")
    if not validate_email(register_form.email.data, relative_path_to_db='DB'):
        error_messages.append("Email is already linked to an account, please use another one")
    if request.method == "POST" and register_form.validate():
        if validate_username(register_form.username.data, relative_path_to_db='DB') and validate_email(
                register_form.email.data, relative_path_to_db='DB'):
            customer = Customer(register_form.username.data, register_form.email.data, register_form.password1.data)
            store_customer(customer_object=customer, relative_path_to_db='DB')
            flash("You have successfully created a new account", category='success')
            return redirect(url_for('home'))
    else:
        for errors in register_form.errors.values():
            error_messages.append(errors[0])
    if error_messages:
        for message in error_messages:
            flash(message, category='danger')
    return render_template('auth/register.html', form=register_form)


@auth.route('/CustomerLogin', methods=["POST", "GET"])
def customer_login():
    login_form = LoginForm()
    if request.method == "POST":
        customer_dict = customer_login_authentication(login_form.username.data, login_form.password.data, 'DB')
        if customer_dict != {}:
            if login_form.remember.data:
                session.permanent = True
            else:
                session.permanent = False
            session['customer'] = customer_dict
            flash(f"Account {login_form.username.data} successfully logged in!", category="success")
            return redirect(url_for('user.customer_dashboard'))
        else:
            flash("Login failed! Please check your username or password again", category='danger')
    return render_template('auth/customer_login.html', form=login_form)


@auth.route('/StaffLogin', methods=["POST", "GET"])
def staff_login():
    login_form = LoginForm()
    if request.method == "POST":
        session['staff'] = login_form.username.data
        flash(f"Account {login_form.username.data} successfully logged in!", category="success")
        return redirect(url_for('user.staff_dashboard'))
    return render_template('auth/staff_login.html', form=login_form)


@auth.route('/logout')
def logout():
    if customer_login_required() or staff_login_required():
        session.pop('customer', None)
        session.pop('staff', None)
        flash("Account has been successfully logged out", category='info')
        return redirect(url_for('home'))
    else:
        restricted_customer_error()
