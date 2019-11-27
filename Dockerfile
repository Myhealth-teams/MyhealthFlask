FROM 119.3.170.97:5000/ubuntu:latest
MAINTAINER pighui pighui233@163.com
WORKDIR /usr/src
RUN git clone git@github.com:Myhealth-teams/MyhealthFlask.git
WORKDIR /usr/src/MyhealthFlask
VOLUME /usr/src/MyhealthFlask/static
RUN pip install -r requirements.txt -i http://mirros.aliyun.com/pypi/simple
RUN pip install gunicorn -i http://mirros.aliyun.com/pypi/simple
RUN chmod +x run.sh
CMD /usr/src/MyhealthFlask/run.sh