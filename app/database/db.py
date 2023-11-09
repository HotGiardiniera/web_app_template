from app.main import app, settings
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = settings.connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def init_db():
    from app.database.models import Account  # noqa
    with app.app_context():
        db.create_all()

