import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Privilege(SqlAlchemyBase):
    __tablename__ = 'privilege'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation("User", back_populates='privilege')


