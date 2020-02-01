import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xd0\x18W$\xda\xe9\xda\xaf]\xda\xb7\xdf\xb9^)M'
    MONGODB_SETTINGS = {'db':'DbCryptoTrading'}