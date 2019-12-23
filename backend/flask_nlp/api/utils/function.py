from flask_nlp import db
from flask_nlp.models import *
from flask import make_response
from wordcloud import WordCloud, STOPWORDS
import base64
from io import BytesIO
import re
import os

JSON_MIME_TYPE = 'application/json'


#分句
def divide_sentence(content):
    content = re.split('(。|！|\!|\.|？|\?)', content)  # 简单分句,保留分割符
    last = ''
    if len(content) % 2 != 0:
        last = content[-1]
    content = [
        content[2 * i] + content[2 * i + 1]
        for i in range(int(len(content) / 2))
    ]  # 将分隔符与句子拼接
    if last != '':
        content.append(last)

    return content


def add_novel(data, keyword):
    novels = Novel.query.filter_by(book_url=data['url']).all()
    for novel in novels:
        db.session.delete(novel)

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

'''
def generate_wordcloud(content):
    stopwords = set(STOPWORDS)

    font_path = '../backend/flask_nlp/static/simsun.ttf'
    font_path = os.path.abspath(font_path)
    font_path = font_path.replace('\\', '/')

    wordcloud = WordCloud(scale=3.5,
                          max_font_size=100,
                          background_color="white",
                          stopwords=stopwords,
                          contour_width=3,
                          max_words=2000,
                          contour_color='steelblue',
                          font_path=font_path).generate(content)
    image = wordcloud.to_image()

    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str
'''
