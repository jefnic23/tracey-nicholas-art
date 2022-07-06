from flask import Flask
from config import Config
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap5
from flask_dropzone import Dropzone
from flask_login import LoginManager
import boto3

# app=Flask(__name__)
# app.config.from_object(Config)
# Talisman(app, content_security_policy=None)
# db = SQLAlchemy(app)
# mail = Mail(app)
# bootstrap = Bootstrap5(app)
# dropzone = Dropzone(app)
# login = LoginManager(app)
# login.init_app(app)


# s3 = boto3.Session(
#     aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
#     aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
# )
# resource = s3.resource('s3', region_name=app.config['AWS_REGION'])
# bucket = resource.Bucket(app.config['BUCKET_NAME'])

# from app import routes, models, errors, views

talisman = Talisman()
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap5()
dropzone = Dropzone()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    talisman.init_app(app, content_security_policy=None)
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    dropzone.init_app(app)
    login.init_app(app)

    # create AWS S3 session
    app.s3 = boto3.Session(
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
    )
    app.resource = app.s3.resource('s3', region_name=app.config['AWS_REGION'])
    app.bucket = app.resource.Bucket(app.config['BUCKET_NAME'])

    # blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models
