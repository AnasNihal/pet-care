from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from app.routes import auth, user, admin, main
    
    # Register blueprints
    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth)
    app.register_blueprint(user.user)
    app.register_blueprint(admin.admin)

    with app.app_context():
        from app import models  # make sure models are registered
        db.create_all()
    
    # Register 404 error handler
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    return app
