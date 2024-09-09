from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd
from flask_login import LoginManager
from flask import Blueprint

db = SQLAlchemy()
if os.environ.get("VERCEL"):
    db_path = "/tmp/app.db"
else:
    db_path = os.path.join(os.getcwd(), "instance", "app.db")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "21133232"
    # qaysi malumotlar bazasiga ulanishi
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)

    # blueprint
    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

