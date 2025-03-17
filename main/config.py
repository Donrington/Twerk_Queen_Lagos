from sqlalchemy import create_engine
import psycopg2
from os import getenv

# user = getenv('AMANIGO_USER')
# password = getenv('AMANIGO_PWD')
# database = getenv('AMANIGO_DB')
# host = getenv('AMANIGO_HOST')


config = {
    'user': 'tql',
    'password': 'zvXDL5HncjJXFpQAi5nXMxmG4orJtCsg',
    'host': 'dpg-cvbn8llds78s73amooi0-a.oregon-postgres.render.com',
    'database': 'twerkqueenlagos'
}

# Connect to PostgreSQL using psycopg2
connection = psycopg2.connect(
    user=config['user'],
    password=config['password'],
    host=config['host'],
    database=config['database']
)


SECRET_KEY = "THTD673&?/YHG/@H393_YEU"
WTF_CSRF_ENABLED= True
ADMIN_EMAIL = "admin@personal.com"
USER_PROFILE_PATH = "main/static/uploads/"
ADMIN_PROFILE_PATH = "main/static/uploads/admins/"
PRODUCT_UPLOADER = "main/static/products/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# SQLALCHEMY_DATABASE_URI=f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
# SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/twerkqueenlagos"

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://tql:zvXDL5HncjJXFpQAi5nXMxmG4orJtCsg@dpg-cvbn8llds78s73amooi0-a.oregon-postgres.render.com/twerkqueenlagos"

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
