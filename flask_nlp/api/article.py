from flask import jsonify, request, current_app, url_for
from flask.blueprints import Blueprint
from ..models import *
from ...spider.spider import CpSpider
from flask_nlp import db
from flask_restful import reqparse, abort, Api, Resource
from utils import *

api = Blueprint('api', __name__)

api.add_resource(BookQueryList, '/cpNlp/api/v1.0/books/queries/[query_id]')
api.add_resource(Book, '/cpNlp/api/v1.0/books/[book_id]')
api.add_resource(ChapterList, '/cpNlp/api/v1.0/chapters')
api.add_resource(Chapter, '/cpNlp/api/v1.0/chapters/[chapter_id]')


class BookQueryList(Resource):
    def put(self, item_id):
        args = parser.parse_args()
        item = {'name': args['name'], 'age': args['age']}
        ITEMS[item_id] = item
        return item, 201

    #根据关键字获取列表
    def post(self, keyword):
        books = Novel.query.filter_by(search_name=search, page=page).all()
        if books:
            return jsonify({'books': [book.to_json() for book in books]})

        spider = CpSpider()
        for data in spider.get_index_result(search, page):
            add_novel(data)

        books = Novel.query.filter_by(search_name=search, page=page).all()
        return jsonify({'books': [book.to_json() for book in books]}), 201


class Book(Resource):
    def put(self, item_id):
        args = parser.parse_args()
        item = {'name': args['name'], 'age': args['age']}
        ITEMS[item_id] = item
        return item, 201

    #根据关键字获取列表
    def get(self, item_id):
        books = Novel.query.filter_by(search_name=search, page=page).all()
        if books:
            return jsonify({'books': [book.to_json() for book in books]}), 200
        else:
            abort(400)


@main.route('/chapter/<int:book_id>')
def chapter(book_id):
    all_chapter = Chapter.query.filter_by(book_id=book_id).first()

    if all_chapter:
        pagination = Chapter.query.filter_by(book_id=book_id).paginate(
            page,
            per_page=current_app.config['CHAPTER_PER_PAGE'],
            error_out=False)
        chapters = pagination.items
        book = Novel.query.filter_by(id=book_id).first()

    spider = CpSpider()
    book = Novel.query.filter_by(id=book_id).first()
    for data in spider.get_chapter(book.book_url):
        add_chapter(data)

    pagination2 = Chapter.query.filter_by(book_id=book_id).paginate(
        page, per_page=current_app.config['CHAPTER_PER_PAGE'], error_out=False)
    chapters = pagination2.items


@api.route('/chapter/<int:book_id>')
def get_chapter(book_id):
    # chapters = Chapter.query.filter_by(book_id=book_id).all()
    page = request.args.get('page', 1, type=int)
    pagination = Chapter.query.filter_by(book_id=book_id).paginate(
        page, per_page=current_app.config['CHAPTER_PER_PAGE'], error_out=False)
    chapters = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_chapter',
                       book_id=book_id,
                       page=page - 1,
                       _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_chapter',
                       book_id=book_id,
                       page=page + 1,
                       _external=True)

    return jsonify({
        'chapters': [chapter.to_json() for chapter in chapters],
        'prev': prev,
        'next': next
    })


@api.route('/content/<int:chapter_id>')
def get_content(chapter_id):
    content = Article.query.get_or_404(chapter_id)
    return jsonify(content.to_json())