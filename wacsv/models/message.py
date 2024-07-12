from datetime import datetime
from dateutil import tz
from dateutil.relativedelta import relativedelta

from flask import current_app

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
        epoch = datetime.fromtimestamp(self.ZMESSAGEDATE)
        epoch = epoch.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
        if current_app.config['WACSV_TZINFO']:
            epoch = epoch.astimezone(tz.gettz(current_app.config['WACSV_TZINFO']))
        return epoch + relativedelta(years=31)
