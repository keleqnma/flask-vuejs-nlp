import os
import json
import unittest

from flask_nlp.api.post import app


class Step1TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        from flask_nlp.models import Search, Novel, Chapter, Article

    def test_book_list(self):
        resp = self.app.post('/cpNlp/api/v1.0/books/keyword/卡比丘')
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        print(content[0])
        self.assertEqual(len(content), 1)
        self.assertEqual(
            content[0], {
                'book_name': '走狗',
                'book_url':
                'https://www.gongzicp.com/https://www.gongzicp.com/novel-250.html',
                'book_img':
                'https://resourcecp.oss-cn-beijing.aliyuncs.com/uploads/20180601/thumb_1e88eaaeec1c2881b2fcafd8ccbb4893.jpg?x-oss-process=style/small',
                'author': '卡比丘',
                'profile': '',
                'type': '青春',
                'time': '更新时间：2017-10-17'
            })

    '''
    def test_book_detail_200(self):
        resp = self.app.get('/book/{}'.format(self.book_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(content, {
            'id': 33,
            'title': 'The Raven',
            'author_id': 1
        })

    def test_book_detail_404(self):
        resp = self.app.get('/book/1111')
        self.assertEqual(resp.status_code, 404)
    '''


if __name__ == "__main__":
    testcase = Step1TestCase()
    testcase.setUp()
    testcase.test_book_list()
