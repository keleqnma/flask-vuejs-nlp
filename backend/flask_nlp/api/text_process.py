# coding=utf-8
import json
from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
from ..models import *
import pkuseg
import jiagu
from .utils import post_dict, generate_wordcloud, ner_dict, divide_sentence
from .text_generate import contentlist

api = Blueprint('api_process', __name__)


@api.route('/segcontent/<int:chapter_id>')
def contentseg(chapter_id):
    wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()
    if wordsegs:
        return jsonify({'words': [word.wordseg for word in wordsegs]}), 200

    content = getContent(chapter_id)
    wordsegs = pkuseg.pkuseg().cut(content)

    for word in wordsegs:
        wordseg = WordSeg(wordseg=word, chapter_id=chapter_id)
        db.session.add(wordseg)

    return jsonify({'words': [word for word in wordsegs]}), 200


@api.route('/senticontent/<int:chapter_id>')
def senticontent(chapter_id):
    senticontents = SentiContent.query.filter_by(chapter_id=chapter_id).all()
    if senticontents == []:
        content = getContent(chapter_id)
        contents_sentences = divide_sentence(content)

        for i, contents_sentence in enumerate(contents_sentences):
            sentiment = jiagu.sentiment(contents_sentence)
            senticontent = SentiContent(sentence=contents_sentences[i],
                                        senti=sentiment[0],
                                        degree=sentiment[1],
                                        chapter_id=chapter_id)
            db.session.add(senticontent)

        senticontents = SentiContent.query.filter_by(
            chapter_id=chapter_id).all()

    return jsonify({
        'sentiments':
        [senticontent.to_json() for senticontent in senticontents]
    }), 200


@api.route('/nercontent/<int:chapter_id>')
def nercontent(chapter_id):
    words = getContentSeg(chapter_id)
    ners = jiagu.ner(words)  # 命名实体识别
    return jsonify(
        {'ners':
         [[words[i], ner_dict[ner]] for i, ner in enumerate(ners)]}), 200


@api.route('/postagcontentseg/<int:chapter_id>')
def contentpostagseg(chapter_id):
    postwordsegs = PostWordSeg.query.filter_by(chapter_id=chapter_id).all()
    if postwordsegs:
        return jsonify(
            {'words':
             [[word.wordseg, word.postag] for word in postwordsegs]}), 200

    content = getContent(chapter_id)
    postwordsegs = pkuseg.pkuseg(postag=True).cut(content)

    for postwordseg in postwordsegs:
        wordseg = PostWordSeg(wordseg=postwordseg[0],
                              postag=post_dict[postwordseg[1]],
                              chapter_id=chapter_id)
        db.session.add(wordseg)

    wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()
    if wordsegs == []:
        for postwordseg in postwordsegs:
            wordseg = WordSeg(wordseg=postwordseg[0], chapter_id=chapter_id)
            db.session.add(wordseg)

    return jsonify(
        {'words':
         [[word[0], post_dict[word[1]]] for word in postwordsegs]}), 200


@api.route('/wordcloud/<int:chapter_id>')
def wordcloud(chapter_id):
    wordsegs = getContentSeg(chapter_id)
    content = " ".join(wordsegs)

    return generate_wordcloud(content)


def getContent(chapter_id):
    content = Content.query.filter_by(chapter_id=chapter_id).first()
    if content:
        return content.content

    contentlist(chapter_id)
    content = Content.query.filter_by(chapter_id=chapter_id).first().content
    return content


def getContentSeg(chapter_id):
    wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()
    if wordsegs == []:
        contentseg(chapter_id)
        wordsegs = WordSeg.query.filter_by(chapter_id=chapter_id).all()

    words = [word.wordseg for word in wordsegs]
    return words