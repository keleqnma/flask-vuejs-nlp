# coding=utf-8
import json
from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
from ..models import *
import pkuseg
from .utils import post_dict, generate_wordcloud
from .text_generate import contentlist
api = Blueprint('api_process', __name__)


@api.route('/segcontent/<int:chapter_id>')
def contentseg(chapter_id):
    wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()
    if wordsegs:
        return jsonify({'words': [word.wordseg for word in wordsegs]}), 200

    content = Content.query.filter_by(chapter_id=chapter_id).first().content
    wordsegs = pkuseg.pkuseg().cut(content)

    for word in wordsegs:
        wordseg = WordSeg(wordseg=word, chapter_id=chapter_id)
        db.session.add(wordseg)

    return jsonify({'words': [word for word in wordsegs]}), 200


@api.route('/postagcontentseg/<int:chapter_id>')
def contentpostagseg(chapter_id):
    postwordsegs = PostWordSeg.query.filter_by(chapter_id=chapter_id).all()
    if postwordsegs:
        return jsonify(
            {'words':
             [[word.wordseg, word.postag] for word in postwordsegs]}), 200

    content = Content.query.filter_by(chapter_id=chapter_id).first().content
    postwordsegs = pkuseg.pkuseg(postag=True).cut(content)

    for postwordseg in postwordsegs:
        wordseg = PostWordSeg(wordseg=postwordseg[0],
                              postag=post_dict[postwordseg[1]],
                              chapter_id=chapter_id)
        db.session.add(wordseg)

    return jsonify(
        {'words':
         [[word[0], post_dict[word[1]]] for word in postwordsegs]}), 200


@api.route('/wordcloud/<int:chapter_id>')
def wordcloud(chapter_id):
    wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()
    if wordsegs:
        content = " ".join([word.wordseg for word in wordsegs])
    else:
        contentseg(chapter_id)
    wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()
    content = " ".join([word.wordseg for word in wordsegs])

    return generate_wordcloud(content)