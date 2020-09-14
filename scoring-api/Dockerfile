FROM ubuntu:18.04

COPY . /usr/src/app/
WORKDIR /usr/src/app

# System packages
RUN apt-get update && apt-get install -y curl default-jre

# Install miniconda to /miniconda

RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}

# Create the environment:
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "wai", "/bin/bash", "-c"]

EXPOSE 5000
