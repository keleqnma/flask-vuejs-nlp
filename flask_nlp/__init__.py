# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_nlp.config import config

#初始化数据库对象
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    # 我们使用app.config对象提供的from_object()方法导入配置
    app.config.from_object(config[config_name])
    # 注册数据库实例
    db.init_app(app)
    # 构造蓝本

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .api.post import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/cpNlp/api/v1.0')

    return app