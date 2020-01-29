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

class Coin(db.Document):
    coin_id = db.IntField(unique=True)
    coin_name = db.StringField(max_length=30)
    value = db.FloatField()

class Transaction(db.Document):
    transaction_id = db.IntField(unique=True)
    transaction_type = db.StringField(max_length=10)
    coin_name = db.StringField(max_length=30)
    amount = db.FloatField()
    value = db.FloatField()
    date = db.DateTimeField()
