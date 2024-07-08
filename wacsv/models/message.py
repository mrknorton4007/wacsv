from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import Boolean, DateTime, Integer, String, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column

from wacsv import db


class Message(db.Model):
    __tablename__ = "ZWAMESSAGE"

    Z_PK = mapped_column(Integer, primary_key=True)
    ZCHATSESSION = mapped_column(ForeignKey('ZWACHATSESSION.Z_PK'))
    # ZMESSAGEDATE = mapped_column(TIMESTAMP(timezone=False))
    ZMESSAGEDATE = mapped_column(Integer)
    ZISFROMME = mapped_column(Boolean)
    ZTEXT = mapped_column(String)

    @hybrid_property
    def ZMESSAGEDATE_LOCAL(self) -> DateTime:
        # ZMESSAGEDATE is an unixepoch timestamp, starting from 1993-01-01
        return datetime.fromtimestamp(self.ZMESSAGEDATE) + relativedelta(years=31)
