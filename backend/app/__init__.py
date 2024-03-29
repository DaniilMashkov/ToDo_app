from datetime import timedelta

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import click
from flask.cli import with_appcontext
from sqlalchemy.dialects import postgresql
from sqlalchemy import column, table
from hashlib import sha256


db = SQLAlchemy()
migrate = Migrate()


app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.Config')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

db.init_app(app)
migrate.init_app(app, db, compare_type=True)
app.app_context().push()

from app.auth import auth
from app.todo import todo
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(todo, url_prefix="/api")

@click.command(name='create_admin')
@with_appcontext
def create_admin():
    t = table('user', column('username'), column('password'))
    insert_stmt = postgresql.insert(t).values(
        username='admin', password=sha256(b"123").hexdigest())

    with db.engine.connect() as conn:
        conn.execute(insert_stmt.compile(dialect=postgresql.dialect()))
        conn.commit()

app.cli.add_command(create_admin)

CORS(app)
