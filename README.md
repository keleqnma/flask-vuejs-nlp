# Flask-vuejs-nlp
本项目是我大数据的大作业，要求是在网站里实现nlp的一些功能。
前端：vue, Jquery, elment-ui
后端：flask
部署：docker-compose
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E6%9E%B6%E6%9E%84%E5%9B%BE.png)

## api展示
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/api%E7%BB%93%E6%9E%9C%E7%A4%BA%E4%BE%8B1.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/api%E7%BB%93%E6%9E%9C%E7%A4%BA%E4%BE%8B2.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/api%E7%BB%93%E6%9E%9C%E7%A4%BA%E4%BE%8B3.png)
## 页面展示
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E9%A6%96%E9%A1%B5.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E4%B9%A6%E7%B1%8D.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E5%9F%BA%E7%A1%80.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E5%B1%8F%E8%94%BD.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E5%88%86%E8%AF%8D.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E5%91%BD%E5%90%8D%E5%AE%9E%E4%BD%93%E8%AF%86%E5%88%AB.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E8%AF%8D%E4%BA%911.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E8%AF%8D%E4%BA%912.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E8%AF%8D%E4%BA%913.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E8%AF%8D%E4%BA%914.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8.png)
![image](https://github.com/keleqnma/flask-vuejs-nlp/blob/master/pics/%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8.png)

## Docker部署
```
git clone https://github.com/keleqnma/flask-vuejs-nlp
cd flask-vuejs-nlp
docker-compose up-d
```
打开 http://localhost:3000/ 查看前端页面，后端的接口和开发环境一样，请看下面的测试api部分
## 开发环境运行
```
git clone https://github.com/keleqnma/flask-vuejs-nlp
cd flask-vuejs-nlp
```
### Backend
#### 项目准备工作

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

##### 迁移更新数据库
```python
python manage.py db migrate -m "v1.0"
python manage.py db upgrade
```

##### 运行

```
python manage.py runserver --host 0.0.0.1
```

##### 测试api

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

### Frontend

#### 项目安装

```
npm install
```

##### 开发选项（一般用这个）

```
npm run serve
```

##### 部署选项

```
npm run build
```

##### 测试

```
npm run test
```

##### 自动修正

```
npm run lint
```

##### 个性化设置

参考 [Configuration Reference](https://cli.vuejs.org/config/).

##### 查看结果

打开 http://localhost:8080 查看