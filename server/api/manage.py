from flask import Flask
from flask_script import Manager
from src import app
from config import ProductionConfig
from flask.cli import FlaskGroup

# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

# from config import ProductionConfig


# db = SQLAlchemy()
# flask_bcrypt = Bcrypt()
# app = create_app(None)
# app.config.from_object(ProductionConfig)
# manager = Manager(app)

# @manager.command
# def run():
#     app.run(host='0.0.0.0', port=8000) # TODO: Not debug=True, do better (config)
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
