from shop import app, db
from flask import Flask, render_template, url_for, request, redirect, flash, session
from shop.models import Items, User
from shop.forms import RegistrationForm, LoginForm, SortItems, CheckoutForm
from flask_login import login_user, logout_user, current_user

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SortItems()
    items = Items.query.all()
    if form.sort_type.data == "price_low":
        items = Items.query.order_by(Items.price.asc())
        return render_template("home.html", title="Home", items = items, form=form)
    elif form.sort_type.data == "price_high":
        items = Items.query.order_by(Items.price.desc())
        return render_template("home.html", title="Home", items = items, form=form)
    elif form.sort_type.data == "eco_low":
        items = Items.query.order_by(Items.eco.desc())
        return render_template("home.html", title="Home", items = items, form=form)

    return render_template("home.html", title="Home", items = items, form=form)

@app.route("/register", methods=["GET","POST"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                flash("Logged in")
                return redirect(url_for("home"))
        flash("Login details are incorrect!")
        return render_template("error_page.html", title="success")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop("cart", None)
    flash("You have been logged out!")
    return redirect(url_for("home"))


@app.route("/moreinfo/<int:item_id>")
def moreinfo(item_id):
    item = Items.query.get_or_404(item_id)
    return render_template("moreinfo.html", title="moreinfo", item=item)


@app.route("/show_cart", methods=['GET', 'POST'])
def show_cart():
    if "basket" not in session:
        return render_template("show_cart.html", cart = {}, total = 0)
    else:
        items = session["basket"]
        basket = {}
        total_price = 0
        total_quantity = 0
        for item in items:
            item = Items.query.get_or_404(item)

            if item.id in basket:
                basket[item.id]["quantity"] += 1
            else:
                basket[item.id] = {"quantity":1, "name": item.name,
                 "price":item.price}

            total_price += item.price
            total_quantity = len(items)
#basket[item.id]["quantity"]
            #total_quantity = sum(item['quantity'] for item in basket.values())
        return render_template("show_cart.html", title='Your Shopping Basket',
         cart = basket,
         total = total_price, total_quantity = total_quantity)


@app.route("/add_to_cart/<int:item_id>", methods=['GET', 'POST'])
def add_to_cart(item_id):
	if current_user.is_anonymous:
		flash('Please login to add to basket')
		return redirect("/login")
	else:
		if "basket" not in session:
			session["basket"] = []
		session["basket"].append(item_id)
		flash("Added to cart successfully!")
		return redirect("/show_cart")

@app.route("/delete/<int:item_id>", methods=['GET', 'POST'])
def delete(item_id):
	if "basket" not in session:
		session["basket"] = []
	session["basket"].remove(item_id)
	flash("removed item from cart!")
	session.modified = True
	return redirect("/show_cart")

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
	form = CheckoutForm()
	if form.validate_on_submit():
		session["basket"] = []
		return redirect(url_for('checkout_success'))
	return render_template('checkout.html', title='Checkout', form=form)


@app.route("/checkout_success", methods=['GET', 'POST'])
def checkout_success():
    return render_template("checkout_success.html", title="success")

@app.route("/error_page", methods=['GET', 'POST'])
def error_page():
    return render_template("error_page.html", title="success")








##
