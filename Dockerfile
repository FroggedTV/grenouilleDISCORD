FROM debian:9

ENTRYPOINT ["/usr/bin/python3", "main.py"]

ENV https_proxy=http://p-goodway:3128/
ENV http_proxy=http://p-goodway:3128/

RUN apt-get update
RUN apt-get install -y python3-dev  python3-pip libffi-dev

COPY requirements.txt .

RUN pip3 install -U -r requirements.txt

WORKDIR /root/discord

RUN mkdir -p /usr/share/discord-data

COPY source .
