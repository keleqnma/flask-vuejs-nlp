from flask_nlp import db
from ..models import *
from flask import make_response
from wordcloud import WordCloud, STOPWORDS
import base64
from io import BytesIO
import re

JSON_MIME_TYPE = 'application/json'
ner_dict = {
    'B-PER': '人名',
    'I-PER': '人名',
    'B-LOC': '地名',
    'I-LOC': '地名',
    'B-ORG': '机构名',
    'I-ORG': '机构名',
    'O': '无'
}

post_dict = {
    'n': '名词',
    't': '时间词',
    's': '处所词',
    'f': '方位词',
    'm': '数词',
    'q': '量词',
    'b': '区别词',
    'r': '代词',
    'v': '动词',
    'a': '形容词',
    'z': '状态词',
    'd': '副词',
    'p': '介词',
    'c': '连词',
    'u': '助词',
    'y': '语气词',
    'e': '叹词',
    'o': '拟声词',
    'i': '成语',
    'l': '习惯用语',
    'j': '简称',
    'h': '前接成分',
    'k': '后接成分',
    'g': '语素',
    'x': '非语素字',
    'w': '标点符号',
    'nr': '人名',
    'ns': '地名',
    'nt': '机构名称',
    'nx': '外文字符',
    'nz': '其它专名',
    'vd': '副动词',
    'vn': '名动词',
    'vx': '形式动词',
    'ad': '副形词',
    'an': '名形词'
}


#分句
def divide_sentence(content):
    content = re.split('(。|！|\!|\.|？|\?)', content)  # 简单分句，保留分割符
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


def generate_wordcloud(content):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        scale=3.5,
        max_font_size=100,
        background_color="white",
        stopwords=stopwords,
        contour_width=3,
        contour_color='steelblue',
        font_path=
        "D:/cyq/Desktop/Junior.1/大数据技术与应用/2017213157-陈玉琪-大作业/flask-vuejs-nlp/backend/flask_nlp/static/simsun.ttf"
    ).generate(content)
    image = wordcloud.to_image()

    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str