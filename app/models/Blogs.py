import sqlalchemy
from sqlalchemy import orm
from datetime import datetime as dt
from .db_session import SqlAlchemyBase


class Blogs(SqlAlchemyBase):
    __tablename__: str = 'blogs'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    content = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=dt.now
    )
