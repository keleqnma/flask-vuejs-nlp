FROM python:3.6.7
WORKDIR /Project/demo
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "--host", "0.0.0.0"]