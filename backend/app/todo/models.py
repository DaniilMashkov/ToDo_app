import sqlalchemy as sa
from app import db


class Task(db.Model):
    __table_args__ = {'extend_existing': True}

    id_task = sa.Column(sa.Integer, primary_key=True, nullable=False)
    body = sa.Column(sa.String(50), nullable=False)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    is_active = sa.Column(sa.Boolean, unique=False, default=True)
    admin_mark = sa.Column(sa.Boolean, unique=False, default=False)

    owner = sa.orm.relationship('User', back_populates='tasks')

    def to_dict(self):
        data = {
            "id_task": self.id_task,
            "body": self.body,
            "username": self.owner.username,
            "email": self.owner.email,
            "is_active": self.is_active,
            "admin_mark": self.admin_mark
        }

        return data

    def from_dict(self, data):
        for field in ["body", "is_active", "admin_mark"]:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_collection_dict(query, page, per_page):
        resources = db.paginate(
            query, page=page, per_page=per_page, error_out=False)

        data = {
            "items": [item.to_dict() for item in resources.items],
            "meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total
            },
        }

        return data

    def __repr__(self):
        return f"""
            task:
                id_task: {self.id_task},
                body: {self.body},
                owner_id: {self.owner_id}
                is_active: {self.is_active}
                admin_mark: {self.admin_mark} 
        """
