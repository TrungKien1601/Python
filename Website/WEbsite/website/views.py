from flask import Blueprint, render_template, flash, redirect, request, jsonify
from .models import Product, Cart, Order
from flask_login import login_required, current_user
from . import db
# from intasend import APIService  # Uncomment and use if API is needed

views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'YOUR_PUBLISHABLE_KEY'
API_TOKEN = 'YOUR_API_TOKEN'


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True)
    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f'Quantity of {item_exists.product.product_name} has been updated')
        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of {item_exists.product.product_name} not updated')
    else:
        new_cart_item = Cart(quantity=1, product_link=item_to_add.id, customer_link=current_user.id)
        try:
            db.session.add(new_cart_item)
            db.session.commit()
            flash(f'{new_cart_item.product.product_name} added to cart')
        except Exception as e:
            print('Item not added to cart', e)
            flash(f'{new_cart_item.product.product_name} has not been added to cart')
    
    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = sum(item.product.current_price * item.quantity for item in cart)
    return render_template('cart.html', cart=cart, amount=amount, total=amount + 200)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity += 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        return jsonify({
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        })


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity -= 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        return jsonify({
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        })


@views.route('/removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)

        return jsonify({
            'amount': amount,
            'total': amount + 200
        })


@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()

    if not customer_cart:
        flash('Your cart is empty.')
        return redirect('/')

    try:
        total = sum(item.product.current_price * item.quantity for item in customer_cart)

        # Uncomment and configure the API service if needed
        # service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
        # create_order_response = service.collect.mpesa_stk_push(phone_number='YOUR_NUMBER', email=current_user.email,
        #                                                         amount=total + 200, narrative='Purchase of goods')

        # Simulated response for testing (remove when using real API)
        create_order_response = {
            'invoice': {'state': 'success'},
            'id': 'sample_payment_id'
        }

        if create_order_response['invoice']['state'].lower() == 'success':
            for item in customer_cart:
                new_order = Order(quantity=item.quantity, price=item.product.current_price,
                                  status='Success', payment_id=create_order_response['id'],
                                  product_link=item.product_link, customer_link=item.customer_link)

                db.session.add(new_order)

                product = Product.query.get(item.product_link)
                product.in_stock -= item.quantity

                db.session.delete(item)

            db.session.commit()

            flash('Order placed successfully!')
            return redirect('/orders')
        else:
            flash('Payment failed. Please try again.')
            return redirect('/')

    except Exception as e:
        db.session.rollback()
        print(e)
        flash('An error occurred while placing your order. Please try again later.')
        return redirect('/')


@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)


@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items,
                               cart=Cart.query.filter_by(customer_link=current_user.id).all()
                               if current_user.is_authenticated else [])

    return render_template('search.html')
