from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app

# Models (schema) will go below

class Example(db.Model):
    """Example table, will have id[PK],example columns"""

    __tablename__ = 'example'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    example_column = db.Column(db.String(50),
                           nullable=False)
    