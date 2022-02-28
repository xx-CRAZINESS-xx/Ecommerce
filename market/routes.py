from flask import render_template, redirect, url_for, flash,request
from flask_login import login_user, logout_user, login_required,current_user

from market import app, db
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from market.models import Item, User


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    sell_form=SellForm()
    purchase_form=PurchaseForm()

    if request.method == 'POST':
        # for purchasing an item
        purchased_item=request.form.get('purchased_item')
        purchased_item_object=Item.query.filter_by(name=purchased_item).first()

        # allows user to purchase an item if there is sufficient amount
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):

            # reduce the budget after purchase of an item and save it to db (function in models.py)
                purchased_item_object.buy(current_user)
                flash(f'You have purchased {purchased_item_object.name}',category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {purchased_item_object.name}",category='danger')

         # for selling an item
        sold_item=request.form.get('sold_item')
        sold_item_object=Item.query.filter_by(name=sold_item).first()

        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                # increases the budget after sale of an item and save it to db (function in models.py)
                sold_item_object.sell(current_user)
                flash(f'You sold {sold_item_object.name}', category='success')

            else:
                flash(f"Something went wrong with selling {sold_item_object.name}",category='danger')

        return redirect(url_for('market_page'))
    if request.method =="GET":
        items = Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form,owned_items=owned_items,sell_form=sell_form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # to check if a user exists and his password matches
        attempted_user=User.query.filter_by(user_name=form.user_name.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.user_name}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Invalid user name or password. Please verify your credentials',category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # to create a new user and save it to the db
        user_to_create = User(user_name=form.user_name.data,
                              email_address=form.email_address.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        # redirect to market page after login or registration
        login_user(user_to_create)
        flash(f'Account created successfully. You are now logged in as {user_to_create.user_name}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:  # to display any errors at the time of registration
        for err_msg in form.errors.values():
            flash(f'Unable to create a user {err_msg}', category='danger')

    return render_template('register.html', form=form)

# to logout and redirect to home page
@app.route('/logout')
def log_out():
    logout_user()
    flash('You have been logged out',category='info')
    return redirect(url_for('home_page'))