FROM ubuntu:18.04
LABEL maintainer="Sultan Yerumbayev <sultan.yerumbayev@gmail.com>"
RUN apt-get update -y
RUN apt-get install -y python3 python3-dev python3-pip wget
RUN apt-get remove -y python-pip python3-pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY entrypoint.sh .
RUN ls -a
RUN chmod 777 entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]

