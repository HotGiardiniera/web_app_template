from sqlalchemy import Column, Integer, String

from app.database.db import db


class Account(db.Model):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
