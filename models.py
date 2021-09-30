from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression, func


"""account = relationship("Account")"""
"""user_id = Column(Integer, ForeignKey('users.id'))"""


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), default='Sahan', server_default='Sahan', unique=False, nullable=True)
    is_admin = Column(Boolean, default=False, server_default=expression.false())
    email = Column(String(120), unique=False, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    account = relationship("Account", back_populates="user")

    def __init__(self, username=None, email=None, is_admin=False):
        self.username = username
        self.email = email
        self.is_admin = is_admin

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'is_admin': self.is_admin}

    def __repr__(self):
        return "<User(username='%s', email='%s', is_admin='%s')>" % (
                                self.username, self.email, self.is_admin)


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="account")
    name = Column(String(80), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name=None, user_id=user_id):
        self.name = name
        self.user_id = user_id

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,  'name': self.name}

    def __repr__(self):
        return '<User %r>' % self.name
