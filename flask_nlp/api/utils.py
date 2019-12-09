from flask_nlp import db
from ..models import *
from flask import make_response

JSON_MIME_TYPE = 'application/json'


def add_novel(data, keyword):
    novel = Novel(book_name=data['title'],
                  book_url=data['url'],
                  book_img=data['image'],
                  author=data['author'],
                  type=data['type'],
                  profile=data['profile'],
                  last_update=data['time'],
                  keyword=keyword)
    db.session.add(novel)


def add_chapter(data, book_id):
    chapter = Chapter(chapter=data['chapter'],
                      chapter_url=data['url'],
                      book_id=book_id)
    db.session.add(chapter)


def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)