from datetime import datetime
from petcare import db
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy_utils import EmailType
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32))
    surname = db.Column(db.String(32))
    role = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime)
    services = db.relationship("Service")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update(user):
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        roles = {
            0: 'User',
            1: 'Seller',
            2: 'Admin'
        }
        return f"<{roles[self.role]} {self.display_name}>"


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<{self.service_name}: {self.description}>"
