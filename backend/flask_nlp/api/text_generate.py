# coding=utf-8
import json
import random
from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
from .utils import add_novel, add_chapter
from ..models import *
from flask_nlp import db
from ..spider.spider import CpSpider

api = Blueprint('api', __name__)


#随机抽取一本小说放在首页
@api.route('/books', methods=['GET'])
def book_random():
    rand = random.randrange(0, Novel.query.count())
    book = Novel.query[rand]
    return jsonify({'books': [book.to_json()]}), 200


@api.route('/books/keyword/<keyword>', methods=['GET', 'POST'])
def book_list(keyword):
    books = Novel.query.filter_by(keyword=keyword).all()
    if books:
        return jsonify({'books': [book.to_json() for book in books]}), 200

    spider = CpSpider()
    for data in spider.get_index_result(keyword, page=0):
        add_novel(data, keyword)

    books = Novel.query.filter_by(keyword=keyword).all()
    return jsonify({'books': [book.to_json() for book in books]}), 200


@api.route('/chapters/<int:book_id>', methods=['GET', 'POST'])
def chapter_list(book_id):
    page = 1
    # page = request.args.get('page', 1, type=int)
    chapters = Chapter.query.filter_by(book_id=book_id).all()

    if chapters:
        return jsonify(
            {'chapters': [chapter.to_json() for chapter in chapters]}), 200

    spider = CpSpider()

    book = Novel.query.filter_by(id=book_id).first()
    print(book)
    for data in spider.get_chapter(book.book_url):
        add_chapter(data, book_id)

    chapters = Chapter.query.filter_by(book_id=book_id).all()

    return jsonify({'chapters':
                    [chapter.to_json() for chapter in chapters]}), 200


@api.route('/chaptercontent/<int:chapter_id>')
def contentlist(chapter_id):
    content = Content.query.filter_by(chapter_id=chapter_id).first()
    if content:
        return jsonify(content.to_json()), 200

    spider = CpSpider()
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    content = Content(content=spider.get_content(chapter.chapter_url),
                      chapter_id=chapter_id)
    db.session.add(content)
    return jsonify(content.to_json()), 200