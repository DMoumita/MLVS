# Dockerfile for nnenum
#
# To build image:
# docker build . -t mlvs_image
#
# To run container image:
# docker run -i mlvs_image bash

FROM python:3.6

COPY ./requirements.txt /MLVS/requirements.txt

# set working directory
WORKDIR /MLVS

# install python package dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

# set environment variables
ENV PYTHONPATH=$PYTHONPATH:/MLVS
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1

# copy remaining files to docker
COPY . /MLVS

# cmd, run one of each benchmark
ENV FLASK_APP  mlvs.py
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
