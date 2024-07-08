from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from wacsv import db


class ChatSession(db.Model):
    __tablename__ = "ZWACHATSESSION"

    Z_PK = mapped_column(Integer, primary_key=True)
    ZPARTNERNAME = mapped_column(String)
    ZMESSAGECOUNTER = mapped_column(Integer)
    ZCONTACTJID = mapped_column(String)
