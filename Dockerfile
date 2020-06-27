FROM ethanhunt314/python-pyserial:3.7-alpine3.12-pyserial3.4

ADD carreralib/ /usr/local/lib/python3.7/site-packages/carreralib/

ENV TERM=linux
ENV TERMINFO=/etc/terminfo


ENTRYPOINT [ "python", "-m", "carreralib", "/dev/ttyUSB0" ]

