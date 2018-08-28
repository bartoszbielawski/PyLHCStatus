from sqlalchemy import Column, String, SmallInteger, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import DB_PATH
Base = declarative_base()


class PyLHCStatus(Base):
    __tablename__ = 'lhcstatus'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    beam_energy = Column(SmallInteger)
    beam_mode = Column(String(64))
    machine_mode = Column(String(64))
    comment = Column(Text)
    timestamp = Column(DateTime, primary_key=True)

    def __str__(self):
        return "{0.timestamp}: {0.beam_mode} - {0.beam_energy:+4d} GeV - {0.comment}".format(self)

    @staticmethod
    def create_db(filename):
        engine = create_engine(filename)
        Base.metadata.create_all(engine)


if __name__ == "__main__":
    PyLHCStatus.create_db(DB_PATH)
