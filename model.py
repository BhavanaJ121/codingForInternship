from database import Base
from sqlalchemy import Column, Integer, String


class Pdfs(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(String)