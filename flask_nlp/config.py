# config.py
# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# wtf表单配置
CSRF_ENABLED = True
SECRET_KEY = 'you-guess'

# 数据库配置
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

DEBUG = True
# 章节页每一页显示的章节数
CHAPTER_PER_PAGE = 20