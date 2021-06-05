# docker build --tag stedsans:1.0 .
# bash: docker run -v /mnt/c/Users/z6hjb/'OneDrive - KMD'/projects/UNI/stedsans:/stedsans --name stedsans -it stedsans:1.0
FROM python:3.8

RUN apt-get update && \
    apt-get install sudo -y

COPY requirements.txt /tmp/

RUN python -m pip install --upgrade pip
RUN python -m pip install -r /tmp/requirements.txt

RUN apt-get update
RUN apt-get install git -y

