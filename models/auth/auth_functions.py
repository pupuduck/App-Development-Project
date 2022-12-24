import shelve
from routes.auth import session, flash
from flask import redirect, url_for
from bcrypt import checkpw


def customer_login_required():
    """Returns True if customer is logged in"""
    if 'customer' in session:
        return True
    else:
        return False


def staff_login_required():
    """Returns True if staff is logged in"""
    if 'staff' in session:
        return True
    else:
        return False


def restricted_customer_error():
    """Flashes error message and redirects user to the login page"""
    flash("Please log in to your account first to access this page", category='danger')
    return redirect(url_for('auth.customer_login'))


def restricted_staff_error():
    """Flashes error message and redirects user to the login page"""
    flash("Please log in to your account first to access this page", category='danger')
    return redirect(url_for('auth.staff_login'))


def validate_username(username_to_validate, relative_path_to_db):
    """Return True if username is not taken, False if username is taken"""
    is_valid = True
    customer_list = get_customers(relative_path_to_db)
    for customer in customer_list:
        if customer.get_username() == username_to_validate:
            is_valid = False
    return is_valid


def validate_email(email_to_validate, relative_path_to_db):
    """Return True if email is not taken, False if username is taken"""
    is_valid = True
    customer_list = get_customers(relative_path_to_db)
    for customer in customer_list:
        if customer.get_email() == email_to_validate:
            is_valid = False
    return is_valid


def get_customers(relative_path_to_db):
    """Returns a list of customer objects"""
    transfer_dict = {}
    customer_list = []
    try:
        db = shelve.open(f"{relative_path_to_db}/user/customer/customer", 'c')
        if "customer" in db:
            transfer_dict = db['customer']
        else:
            db['customer'] = transfer_dict
    except IOError:
        print("Error occurred while trying to open the shelve file")
    except Exception as ex:
        print(f"Error occurred as {ex}")
    for customer in transfer_dict.values():
        customer_list.append(customer)
    return customer_list


def store_customer(customer_object, relative_path_to_db):
    """Stores customer object inside the customer database"""
    try:
        transfer_dict = {}
        db = shelve.open(f"{relative_path_to_db}/user/customer/customer", 'c')
        if "customer" in db:
            transfer_dict = db['customer']
        else:
            db['customer'] = transfer_dict
        transfer_dict[customer_object.get_user_id()] = customer_object
        db['customer'] = transfer_dict
        db.close()
    except IOError:
        print("Error occurred while trying to open the shelve file")
    except Exception as ex:
        print(f"Error occurred as {ex}")


def customer_login_authentication(username_email, password, relative_path_to_db):
    """Checks if customer login matches the database and returns valid (T or F) and a dictionary of the customer
    object """
    customer_dict = {}
    customers = get_customers(relative_path_to_db)
    for customer in customers:
        if customer.get_email() == username_email or customer.get_username() == username_email:
            if checkpw(password.encode(), customer.get_password_hash()):
                customer_dict = vars(customer)
    return customer_dict
