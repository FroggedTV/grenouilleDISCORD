FROM debian:9

ENTRYPOINT ["/usr/bin/python3", "main.py"]

RUN apt-get update
RUN apt-get install -y python3-dev  python3-pip libffi-dev

COPY requirements.txt .

RUN pip3 install -U -r requirements.txt

WORKDIR /root/discord

COPY source .
