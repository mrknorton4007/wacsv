from sqlalchemy import BLOB, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from wacsv import db


class MediaItem(db.Model):
    __tablename__ = "ZWAMEDIAITEM"

    Z_PK = mapped_column(Integer, primary_key=True)
    ZMESSAGE = mapped_column(Integer, ForeignKey('ZWAMESSAGE.Z_PK'))
    ZTITLE = mapped_column(String)
    ZVCARDSTRING = mapped_column(String)
    ZMEDIALOCALPATH = mapped_column(String)
    ZMEDIAURL = mapped_column(String)
    ZMEDIAKEY = mapped_column(BLOB)
    ZMETADATA = mapped_column(BLOB)
