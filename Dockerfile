FROM python:3.8-slim-buster

RUN mkdir /app

COPY . /app/

RUN cd /app \
    && python3 -m pip install --upgrade pip\
    && pip3 install --no-cache-dir -r requirements.txt\
    && rm -rf /tmp/* && rm -rf /root/.cache/*
# 设置系统时区

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

WORKDIR /app

CMD ["python3", "app.py"]
