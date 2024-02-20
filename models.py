import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
def drop_tables(engine):
    Base.metadata.drop_all(engine)
def create_tables(engine):
    Base.metadata.create_all(engine)
class CAN_package(Base):
    __tablename__ = "package"
    id = sq.Column(sq.Integer, primary_key=True)
    data_length = sq.Column(sq.String(length=15))
    PGN = sq.Column(sq.Integer, unique=True)
    ID = sq.Column(sq.String(length=15), unique=True)

class Parameter(Base):
    __tablename__ = "parameter"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80))
    length = sq.Column(sq.String(length=15))
    scaling = sq.Column(sq.String(length=15))
    range = sq.Column(sq.String(length=15))
    SPN = sq.Column(sq.Integer)
    id_CAN = sq.Column(sq.Integer, sq.ForeignKey("package.PGN"), nullable=False)
    package = relationship(CAN_package, backref="parameters")
