FROM arm32v7/python:3.7-alpine3.12

ADD carreralib/ /usr/local/lib/python3.7/site-packages/carreralib/

RUN pip install pyserial==3.4

ENV TERM=linux
ENV TERMINFO=/etc/terminfo


ENTRYPOINT [ "python", "-m", "carreralib", "/dev/ttyUSB0" ]

