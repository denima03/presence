# pull official base image
FROM python:3.10-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql curl \
  && apt-get clean

# install python dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

# export to requirements
COPY pyproject.toml .
RUN ~/.local/bin/poetry export -f requirements.txt --output requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# add app
RUN cd /usr/src/app
COPY app/. .
COPY entry-point/start.sh .
RUN chmod +x start.sh 
ENTRYPOINT [ "/usr/src/app/start.sh" ]
CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]

