FROM ethanhunt314/python-pyserial:3.7-alpine3.12-pyserial3.4

ADD carreralib/ /usr/local/lib/python3.7/site-packages/carreralib/
ADD skyhopper/  /opt/skyhopper/

#ENV TERM=linux
#ENV TERMINFO=/etc/terminfo
#ENTRYPOINT [ "python", "/opt/skyhopper/main.py" ]

