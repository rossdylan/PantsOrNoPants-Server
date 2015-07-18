from sqlalchemy import (Column,
                        String,
                        Integer,
                        Float,
                        ForeignKey,
                        Table,
                        relationship,
                        DateTime)

from ponp_server.database import Base


assoc_table = Table('association', Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('report_id', Integer, ForeignKey('pcireports.id')))


class PCIReport(Base):
    __tablename__ = 'pcireports'
    id = Column(Integer, primary_key=True)
    user = relationship("User", secondary=assoc_table)
    lat = Column(Float)
    lng = Column(Float)
    height = Column(Float)
    weight = Column(Float)
    datetime = Column(DateTime)
    pci = Column(Float)
