# coding=utf-8
import json
from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
from ..models import *
# import pkuseg
import jiagu
from .utils.function import divide_sentence
from .utils.variable import post_dict, ner_dict, stop_words
from .text_generate import contentlist

api = Blueprint('api_process', __name__)


#分词结果
@api.route('/segcontent/<int:chapter_id>')
def contentseg(chapter_id):
    contents_sentences = getContentSentence(chapter_id)

    if WordSeg.query.filter_by(
            sentence_id=contents_sentences[0].id).all() == []:
        #切割句子
        for contents_sentence in contents_sentences:
            #wordsegs = pkuseg.pkuseg().cut(contents_sentence.sentenceseg)
            wordsegs = jiagu.seg(contents_sentence.sentenceseg)
            for word in wordsegs:
                wordseg = WordSeg(wordseg=word,
                                  sentence_id=contents_sentence.id)
                db.session.add(wordseg)

    wordsegss = [[word.wordseg for word in contents_sentence.words]
                 for contents_sentence in contents_sentences]
    return jsonify({'words': wordsegss}), 200


# 情感分析
@api.route('/senticontent/<int:chapter_id>')
def senticontent(chapter_id):
    contents_sentences = getContentSentence(chapter_id)

    if SentiContent.query.filter_by(
            sentence_id=contents_sentences[0].id).all() == []:
        for i, contents_sentence in enumerate(contents_sentences):
            sentiment = jiagu.sentiment(contents_sentence.sentenceseg)
            senticontent = SentiContent(senti=sentiment[0],
                                        degree=sentiment[1],
                                        sentence_id=contents_sentence.id)
            db.session.add(senticontent)

    senticontents = [{
        'sentence': contents_sentence.sentenceseg,
        'sentiment': senticontent.senti,
        'degree': senticontent.degree
    } for contents_sentence in contents_sentences
                     for senticontent in contents_sentence.senti]

    return jsonify({'sentiments': senticontents}), 200


@api.route('/postagcontentseg/<int:chapter_id>')
def contentpostagseg(chapter_id):
    wordsegss = getContentSeg(chapter_id)

    if PostWordSeg.query.filter_by(word_id=wordsegss[0][0].id).all() == []:
        for wordsegs in wordsegss:
            poss = jiagu.pos([wordseg.wordseg for wordseg in wordsegs])  # 词性标注
            for i, pos in enumerate(poss):
                wordseg = PostWordSeg(postag=post_dict[pos],
                                      word_id=wordsegs[i].id)
                db.session.add(wordseg)

    tags = [[
        PostWordSeg.query.filter_by(word_id=wordseg.id).first().postag
        for wordseg in wordsegs
    ] for wordsegs in wordsegss]

    return jsonify({'tags': tags}), 200


@api.route('/wordcloud/<int:chapter_id>')
def wordcloud(chapter_id):
    wordsegss = getContentSeg(chapter_id)
    words = [wordseg.wordseg for wordsegs in wordsegss for wordseg in wordsegs]
    words_set = set(words)
    res = []
    for word in words_set:
        if word not in stop_words:
            count = words.count(word)
            res.append({'word': word, 'count': count})

    res.sort(key=lambda x: x['count'], reverse=True)
    # 排序 做到词频高的在中间
    # 只取前两千个词
    if len(res) > 2000:
        res = res[0:2000]
    return jsonify(res), 200


@api.route('/nercontent/<int:chapter_id>')
def nercontent(chapter_id):
    wordsegss = getContentSeg(chapter_id)

    if NerWordSeg.query.filter_by(word_id=wordsegss[0][0].id).all() == []:
        for wordsegs in wordsegss:
            ners = jiagu.ner([wordseg.wordseg for wordseg in wordsegs])  # 词性标注
            for i, ner in enumerate(ners):
                wordseg = NerWordSeg(nertag=ner_dict[ner],
                                     word_id=wordsegs[i].id)
                db.session.add(wordseg)

    ners = [[
        NerWordSeg.query.filter_by(word_id=wordseg.id).first().nertag
        for wordseg in wordsegs
    ] for wordsegs in wordsegss]

    return jsonify({'ners': ners}), 200


#获取内容
def getContent(chapter_id):
    content = Content.query.filter_by(chapter_id=chapter_id).first()
    if content:
        return content.content

    contentlist(chapter_id)
    content = Content.query.filter_by(chapter_id=chapter_id).first().content
    return content


#获取章节分词结果
def getContentSeg(chapter_id):
    contents_sentences = getContentSentence(chapter_id)

    if WordSeg.query.filter_by(
            sentence_id=contents_sentences[0].id).all() == []:
        contentseg(chapter_id)

    wordsegss = [[word for word in contents_sentence.words]
                 for contents_sentence in contents_sentences]
    return wordsegss


#获取章节分句结果
def getContentSentence(chapter_id):
    contents_sentences = SentenceSeg.query.filter_by(
        chapter_id=chapter_id).all()

    if contents_sentences == []:
        content = getContent(chapter_id)
        contents_sentences = divide_sentence(content)

        for contents_sentence in contents_sentences:
            sentenceSeg = SentenceSeg(sentenceseg=contents_sentence,
                                      chapter_id=chapter_id)
            db.session.add(sentenceSeg)
            contents_sentences = SentenceSeg.query.filter_by(
                chapter_id=chapter_id).all()

    return contents_sentences
