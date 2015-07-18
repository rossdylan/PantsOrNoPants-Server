from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType
from ponp_server.database import Base, db_session
from ponp_server.models.reports import assoc_table
from ponp_server.utils import generate_apikey


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    lang = Column(String(10), default='en')
    username = Column(String(20))
    home_lat = Column(Float)
    home_lng = Column(Float)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    apikey = Column(String(65))
    height = Column(Float)
    weight = Column(Float)
    gender = Column(String(10))
    inclination = Column(String(7))
    reports = relationship("PCIReport", secondary=assoc_table)

    @staticmethod
    def new_user(name, passw):
        new = User(username=name,
                   password=passw,
                   apikey=generate_apikey(name))
        db_session.add(new)
        db_session.commit()
        return new

    def to_dict(self):
        return {
            'id': self.id,
            'lang': self.lang,
            'username': self.username,
            'home_lat': self.home_lat,
            'home_lng': self.home_lng,
            'apikey': self.apikey,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'inclination': self.inclination, }

    def __repr__(self):
        return "<User {0} {1:d}>".format(self.username, self.id)
