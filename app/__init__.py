from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Configuration)
    db.init_app(app)
    
    from .blueprint.home import main
    from .blueprint.articles import views
    
    app.register_blueprint(main, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')
    
    return app