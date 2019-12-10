# coding=utf-8
import json
from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
from ..models import *
import pkuseg
from .text_generate import contentlist
api = Blueprint('api_process', __name__)


@api.route('/segcontent/<int:chapter_id>')
def contentseg(chapter_id):
    content = Content.query.filter_by(chapter_id=chapter_id).first().content

    contentsegs = pkuseg.pkuseg().cut(content)
    return jsonify({'words': [word for word in contentsegs]}), 200


@api.route('/postagcontentseg/<int:chapter_id>')
def contentpostagseg(chapter_id):
    content = Content.query.filter_by(chapter_id=chapter_id).first().content

    contentsegs = pkuseg.pkuseg(postag=True).cut(content)
    return jsonify({'words': [word for word in contentsegs]}), 200
