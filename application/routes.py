from application import app, db, api
from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import User, Coin, Transaction
from application.forms import RegisterForm, LoginForm
from flask_restplus import Resource
from datetime import datetime



#########################################################

@api.route('/api','/api/')
class GetAndPost(Resource):

    #GET ALL
    def get(self):
        return jsonify(User.objects.all())

    #POST
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))


@api.route('/api/<idx>')
class GetUpdateAndDelete(Resource):
    
    #GET ONE
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    #PUT
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=data['user_id']))

    #DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

##########################################################

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/logout")
def logout():
    session['user_id'] = False
    session['username'] = False
    return redirect(url_for("index"))

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, You are successfully login!",category="success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect(url_for("index"))
        else:
            flash("Sorry, something went wrong!", category="danger")
            return redirect("/login")
    return render_template("login.html",title="Login", form=form, login=True)

@app.route("/register", methods=['GET','POST'])
def register():
    if session.get('username'):
        return redirect(url_for("index"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        flash("You are successfully registered!",category="success")
        session['user_id'] = user.user_id
        session['username'] = user.first_name
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/transaction", methods=["GET","POST"])
def transaction():
    if not session.get('username'):
        return redirect(url_for("login"))
    transaction_type = request.form.get("transaction_type")
    coin_name = request.form.get("coin_name")
    amount = request.form.get("amount")
    value = calculate_value(coin_name, amount)

    user_id = session['user_id']

    if transaction_type:
        Transaction(user_id=user_id,transaction_type=transaction_type,coin_name=coin_name,amount=amount,value=value,date=datetime.now).save()
        flash(f"Transaction added succesfully",category="success")

    transactions = list(Transaction.objects.aggregate(*[
                    {
                        '$match': {
                            'user_id': session["user_id"]
                        }
                    }, {
                        '$sort': {
                            'date': 1
                        }
                    }
                ]))

    return render_template("transaction.html", transactions=transactions, transaction=True)

@app.route("/coins/")
def coins():
    coins_for_trade = Coin.objects.order_by("+coin_name")
    return render_template("coins.html", coins_for_trade=coins_for_trade, coins=True)

def calculate_value(coin_name, amount):
    return 100