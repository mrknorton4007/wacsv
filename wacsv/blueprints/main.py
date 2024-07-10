from flask import request, render_template, redirect, url_for, abort
from flask import Blueprint

from wacsv.models.chat_session import ChatSession
from wacsv.models.message import Message
from wacsv import db

bp = Blueprint('main', __name__)


@bp.get('/')
def index():
    records = db.session.execute(db.select(ChatSession).order_by(ChatSession.Z_PK)).scalars()
    return render_template('index.html', records=records)


@bp.get('/chat/<int:chat_session_id>', defaults={'page': 1})
@bp.get('/chat/<int:chat_session_id>/<int:page>')
def view_chat(chat_session_id, page):
    chat = db.get_or_404(ChatSession, chat_session_id)
    records = db.paginate(
        select=db.select(Message).filter_by(ZCHATSESSION=chat.Z_PK).order_by(Message.ZMESSAGEDATE),
        page=page, per_page=200, max_per_page=300, error_out=False
    )
    return render_template('chat.html', chat=chat, records=records)
