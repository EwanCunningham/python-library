FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-venv

COPY . /python-library
WORKDIR /python-library

# Runs in dev mode - should be updated to run as production app
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install -r /python-library/requirements.txt

EXPOSE 5000

CMD ["flask", "run"]
