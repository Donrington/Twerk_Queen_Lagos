from sqlalchemy import create_engine
import psycopg2
from os import getenv

# user = getenv('AMANIGO_USER')
# password = getenv('AMANIGO_PWD')
# database = getenv('AMANIGO_DB')
# host = getenv('AMANIGO_HOST')


# config = {
#     'user': 'tql',
#     'password': 'zvXDL5HncjJXFpQAi5nXMxmG4orJtCsg',
#     'host': 'dpg-cvbn8llds78s73amooi0-a.oregon-postgres.render.com',
#     'database': 'twerkqueenlagos'
# }


config = {
    'user': 'doadmin',
    'password': ' AVNS_TP_LtQ97GH9yS3cHm2O',
    'host': 'app-549e29aa-2f2e-49f3-8e0b-5a38d226801c-do-user-19983151-0.l.db.ondigitalocean.com',
    'port': 25060,
    'database': 'defaultdb'
}


# config = {
#     'user': 'doadmin',
#     'password': ' AVNS_TP_LtQ97GH9yS3cHm2O',
#     'host': 'app-549e29aa-2f2e-49f3-8e0b-5a38d226801c-do-user-19983151-0.l.db.ondigitalocean.com',
#     'database': 'defaultdb'
# }



# # Connect to PostgreSQL using psycopg2
# connection = psycopg2.connect(
#     user=config['user'],
#     password=config['password'],
#     host=config['host'],
#     port=config['port'],
#     database=config['database']
# )


# Load from env if possible
DATABASE_USER = 'doadmin'
DATABASE_PASSWORD = 'AVNS_TP_LtQ97GH9yS3cHm2O'
DATABASE_HOST = 'app-549e29aa-2f2e-49f3-8e0b-5a38d226801c-do-user-19983151-0.l.db.ondigitalocean.com'
DATABASE_PORT = '25060'
DATABASE_NAME = 'defaultdb'

SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://doadmin:AVNS_TP_LtQ97GH9yS3cHm2O"
    "@app-549e29aa-2f2e-49f3-8e0b-5a38d226801c-do-user-19983151-0.l.db.ondigitalocean.com:25060/defaultdb?sslmode=require"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
WTF_CSRF_ENABLED= True
ADMIN_EMAIL = "admin@personal.com"
USER_PROFILE_PATH = "main/static/uploads/"
ADMIN_PROFILE_PATH = "main/static/uploads/admins/"
PRODUCT_UPLOADER = "main/static/products/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# SQLALCHEMY_DATABASE_URI=f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
# SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/twerkqueenlagos"

# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://tql:zvXDL5HncjJXFpQAi5nXMxmG4orJtCsg@dpg-cvbn8llds78s73amooi0-a.oregon-postgres.render.com/twerkqueenlagos"



# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://doadmin:AVNS_TP_LtQ97GH9yS3cHm2O@app-549e29aa-2f2e-49f3-8e0b-5a38d226801c-do-user-19983151-0.l.db.ondigitalocean.com:25060/defaultdb"

STRIPE_PUBLISHABLE_KEY = 'your_publishable_key'
STRIPE_SECRET_KEY = 'your_secret_key'


MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USERNAME='carryoby@gmail.com'
MAIL_PASSWORD='pzvw jfdf swwa lmcw'
MAIL_USE_SSL=False
MAIL_USE_TSL=True


FACEBOOK_OAUTH_CLIENT_ID = "YOUR_FACEBOOK_CLIENT_ID"
FACEBOOK_OAUTH_CLIENT_SECRET = "YOUR_FACEBOOK_CLIENT_SECRET"
GOOGLE_OAUTH_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
GOOGLE_OAUTH_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"

PAYSTACK_PUBLIC_KEY = "pk_test_ee3f372887047be287a0769ebc7e8066ea8adc8f"
PAYSTACK_SECRET_KEY = "sk_test_f3f650ddd241d9c89f13c3d9468162052fcc8152"
PAYSTACK_CALLBACK_URL = "https://rokeyla.onrender.com/payment/verify"
