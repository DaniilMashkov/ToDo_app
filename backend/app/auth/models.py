import sqlalchemy as sa
from app import db, jwt



class User(db.Model):
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    username = sa.Column(sa.String(20), nullable=False, unique=True)
    email = sa.Column(sa.String, unique=True, index=True)
    password = sa.Column(sa.String, nullable=True)
    is_admin = sa.Column(sa.Boolean, unique=False, default=False)

    tasks = sa.orm.relationship('Task', back_populates='owner')

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()

    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin
        }

        return data

    def from_dict(self, data):
        for field in ["username", "email", "is_admin"]:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f"""
            user:
                id: {self.id},
                username: {self.username},
                email: {self.email},
                is_admin: {self.is_admin}
        """
