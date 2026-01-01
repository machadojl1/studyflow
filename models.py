from sqlalchemy import create_engine, Column, func, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///subjects.db")

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    sessions = relationship('StdSession', back_populates="subject")


class StdSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    date = Column(Date, server_default=func.current_date())
    notes = Column(String, nullable=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    subject = relationship('Subject', back_populates="sessions")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close()