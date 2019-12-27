# Backend

## 项目准备工作
```python
#建立新虚拟环境(conda也可以，我用的是virtualenv)
pip install virtualenvwrapper#虚拟环境管理包
virtualenv flask-vuejs-nlp

#进入激活虚拟环境
#1.如果安装virtualenvwrapper
workon flask-vuejs-nlp 
#2.如果没安装virtualenvwrapper，使用虚拟环境的激活脚本
\path\to\env\Scripts\activate

#安装依赖包
pip install -r requirements.txt
```

### 迁移更新数据库
```python
python manage.py db migrate -m "v1.0"
python manage.py db upgrade
```

### 运行
```
python manage.py runserver --host 0.0.0.1
```

### 测试api
| http方法 | api列表                                                      | 描述                       |
| -------- | ------------------------------------------------------------ | -------------------------- |
| GET      | localhost:5000/cpNlp/api/v1.0/books                          | 获取缓存小说列表随机十本书 |
| GET      | localhost:5000/cpNlp/api/v1.0/books/[keyword]                | 通过关键字获取小说列表     |
| GET      | localhost:5000/cpNlp/api/v1.0/books/[int:book_id]            | 获取某本小说的详细信息     |
| GET      | localhost:5000/cpNlp/api/v1.0/chapters/[int:book_id]         | 获取某本小说的章节列表     |
| GET      | localhost:5000/cpNlp/api/v1.0/chaptercontent/[int:chapter_id] | 获取某个章节               |
| GET      | localhost:5000/cpNlp/api/v1.0/process/segcontent/[int:chapter_id] | 某个章节的分词结果         |
| GET      | localhost:5000/cpNlp/api/v1.0/process/postagcontentseg/[int:chapter_id] | 某个章节的词性标注         |
| GET      | localhost:5000/cpNlp/api/v1.0/process/nercontent/[int:chapter_id]/ | 某个章节的命名实体识别     |
| GET      | localhost:5000/cpNlp/api/v1.0/process/senticontent/[int:chapter_id]/ | 某个章节的情感分析         |
| GET      | localhost:5000/cpNlp/api/v1.0/process/wordcloud/[int:chapter_id] | 某个章节的词云展示         |


