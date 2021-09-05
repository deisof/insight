import sqlalchemy
from data.db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = 'test'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login_teacher = sqlalchemy.Column(sqlalchemy.String)
    login_student = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    result = sqlalchemy.Column(sqlalchemy.String)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


