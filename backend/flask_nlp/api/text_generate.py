# coding=utf-8
import json
import random
from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
from .utils.function import add_novel, add_chapter
from ..models import *
from flask_nlp import db
from ..spider.spider import CpSpider

api = Blueprint('api', __name__)

spider = CpSpider()


#随机抽取十本小说放在首页
@api.route('/books', methods=['GET'])
def book_random():
    rand = random.randrange(0, Novel.query.count() - 10)
    books = Novel.query.filter(Novel.id >= rand).limit(10).all()
    return jsonify({'books': [book.to_json() for book in books]}), 200


@api.route('/books/<int:book_id>', methods=['GET'])
def book_one(book_id):
    book = Novel.query.filter_by(id=book_id).first()
    return jsonify(book.to_json()), 200


@api.route('/books/keyword/<keyword>', methods=['GET', 'POST'])
def book_list(keyword):
    books = Novel.query.filter_by(keyword=keyword).all()
    if books:
        return jsonify({'books': [book.to_json() for book in books]}), 200

    for data in spider.get_index_result(keyword, page=0):
        add_novel(data, keyword)

    books = Novel.query.filter_by(keyword=keyword).all()
    return jsonify({'books': [book.to_json() for book in books]}), 200


@api.route('/chapters/<int:book_id>', methods=['GET', 'POST'])
def chapter_list(book_id):
    chapters = Chapter.query.filter_by(book_id=book_id).all()

    if chapters == []:

        book = Novel.query.filter_by(id=book_id).first()
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

    chapter = Chapter.query.filter_by(id=chapter_id).first()
    content = Content(content=spider.get_content(chapter.chapter_url),
                      chapter_id=chapter_id)
    db.session.add(content)
    return jsonify(content.to_json()), 200
