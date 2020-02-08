from application import db
import flask
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class Currency(db.Document):
    currency_name = db.StringField(max_length=30)
    currency_symbol = db.StringField(max_length=30)

class Transaction(db.Document):
    user_id = db.IntField()
    transaction_type = db.StringField(max_length=10)
    currency_symbol = db.StringField(max_length=30)
    amount = db.FloatField()
    value = db.FloatField()
    date = db.DateTimeField()
