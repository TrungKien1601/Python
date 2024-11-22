from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        # Kiểm tra mật khẩu có trùng nhau không
        if password1 == password2:
            # Kiểm tra nếu email đã tồn tại
            existing_customer = Customer.query.filter_by(email=email).first()
            if existing_customer:
                flash('Email already exists. Please log in or use a different email.', 'danger')
                return redirect('/login')

            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password1  # Lưu mật khẩu đã mã hóa

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully! You can now log in.', 'success')
                return redirect('/login')
            except Exception as e:
                db.session.rollback()  # Rollback nếu có lỗi
                print(e)
                flash('Account creation failed. Please try again.', 'danger')
        else:
            flash('Passwords do not match!', 'danger')

        # Reset form fields sau khi có lỗi
        form.email.data = ''
        form.username.data = ''
        form.password1.data = ''
        form.password2.data = ''

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer and customer.verify_password(password):  # verify_password() phải là phương thức trong model Customer
            login_user(customer)
            return redirect('/')
        else:
            flash('Incorrect email or password.', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect('/')


@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:  # Kiểm tra nếu customer tồn tại
        return render_template('profile.html', customer=customer)
    else:
        flash('Profile not found.', 'danger')
        return redirect('/')


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = PasswordChangeForm()
    customer = Customer.query.get(customer_id)
    if not customer:
        flash('Customer not found!', 'danger')
        return redirect('/')

    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):  # verify_password() phải là phương thức trong model Customer
            if new_password == confirm_new_password:
                customer.password = new_password  # Lưu mật khẩu đã mã hóa
                db.session.commit()
                flash('Password updated successfully!', 'success')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New passwords do not match!', 'danger')
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('change_password.html', form=form)
