from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

from sc_server_auth.config import db_engines, db_params
from sc_server_auth.server import constants as cnt

Base = declarative_base()


# class Role(Base):
#     __tablename__ = cnt.ROLE
#     id = Column(Integer, primary_key=True, unique=True)
#     name = Column(String(255), nullable=False)
#     users = relationship(cnt.USER)


class User(Base):
    __tablename__ = cnt.USER
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    # role_id = Column(Integer, ForeignKey(f"{cnt.ROLE}.id"))

    def __repr__(self):
        return "<id={}, name={}>".format(self.id, self.name)

    @property
    def serialize(self):
        return {cnt.ID: self.id, cnt.NAME: self.name}


class DataBase:
    def __init__(self) -> None:
        self.engine = db_engines[db_params[cnt.DATABASE]]()
        self.session = None
        Base.metadata.create_all(self.engine, checkfirst=True)
        self._session().commit()

    def _session(self):
        if not self.session:
            self.session = sessionmaker(bind=self.engine)()
        return self.session

    def is_user_valid(self, name, password):
        selected_user = self._session().query(User).filter(User.name == name, User.password == password).first()
        return selected_user is not None

    def is_such_user_in_base(self, name):
        selected_user = self._session().query(User).filter(User.name == name).first()
        return selected_user is not None

    def get_users(self):
        users_info = self._session().query(User)
        users_info = [x.serialize for x in users_info.all()]
        return users_info

    def add_user(self, name: str, password: str) -> bool:
        new_user = User(name=str(name), password=str(password))
        try:
            self._session().add(new_user)
            self._session().commit()
        except IntegrityError:
            return False
        return True

    def delete_user_by_name(self, name: str) -> int:
        delete_users_count = self._session().query(User).filter(User.name == name).delete()
        self._session().commit()
        return delete_users_count

    def update_user_by_name(self, name: str, new_name: str, password: str) -> bool:
        updated_users_count = (
            self._session().query(User).filter(User.name == name).update({cnt.NAME: new_name, cnt.PASSWORD: password})
        )
        self._session().commit()
        return updated_users_count
