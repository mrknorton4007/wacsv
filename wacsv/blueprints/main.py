import os

from flask import abort, redirect, render_template, request, send_file, url_for
from flask import Blueprint
from flask import current_app

from wacsv.models.chat_session import ChatSession
from wacsv.models.media_item import MediaItem
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
    per_page = current_app.config.get('WACSV_PAGINATION', 200)
    records = db.paginate(
        select=db.select(Message).filter_by(ZCHATSESSION=chat.Z_PK).order_by(Message.ZMESSAGEDATE),
        page=page, per_page=per_page, max_per_page=300, error_out=False
    )
    return render_template('chat.html', chat=chat, records=records)


@bp.get('/raw/<int:chat_session_id>')
def view_raw(chat_session_id):
    chat = db.get_or_404(ChatSession, chat_session_id)
    query = db.select(Message).filter_by(ZCHATSESSION=chat.Z_PK).order_by(Message.ZMESSAGEDATE)
    records = db.session.execute(query).scalars()
    return render_template('raw.html', chat=chat, records=records)


@bp.get('/media/<int:media_item_id>')
def view_media(media_item_id):
    media_item = db.get_or_404(MediaItem, media_item_id)
    media_path = os.path.join(current_app.instance_path, media_item.ZMEDIALOCALPATH)
    return send_file(media_path, mimetype=media_item.ZVCARDSTRING)


@bp.get('/permalink/<int:message_id>')
def view_permalink(message_id):
    per_page = current_app.config.get('WACSV_PAGINATION', 200)
    record = db.get_or_404(Message, message_id)
    chat_messages = Message.query.filter(Message.ZCHATSESSION == record.ZCHATSESSION).order_by(Message.ZMESSAGEDATE)
    record_index = chat_messages.all().index(record)
    page = (record_index // per_page) + 1
    anchor = f'msg{ record.Z_PK }'
    return redirect(url_for('main.view_chat', chat_session_id=record.ZCHATSESSION, page=page, _anchor=anchor))


@bp.get('/search')
def view_search():
    search_term = request.args.get('q', None)
    chat_session_id = request.args.get('chat_id', None)
    page = request.args.get('page', 1, type=int)
    if not search_term:
        abort(400)  # bad request
    search_query = Message.query.filter(Message.ZTEXT.ilike(f'%{search_term}%'))
    if chat_session_id:
        search_query = search_query.filter(Message.ZCHATSESSION == chat_session_id)
    search_query = search_query.order_by(Message.ZMESSAGEDATE)
    records = search_query.paginate(page=page, per_page=50, max_per_page=100, error_out=False)
    return render_template('search.html', records=records, q=search_term, chat_id=chat_session_id, page=page)
