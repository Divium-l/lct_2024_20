FROM ubuntu:24.10

RUN apt-get update

RUN apt-get install -y \
    build-essential \
    curl \
    python3 \
    python3-pip \
    libpq-dev \
    python3-dev \
    postgresql-16 \
    postgresql-contrib-16




RUN apt-get update
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app
RUN pip install -r hackaton/requirements.txt --break-system-packages
RUN pip install transformers --break-system-packages
RUN python3 hackaton/manage.py migrate

EXPOSE 8000

CMD ["python3", "hackaton/manage.py", "runserver", "0.0.0.0:8000" ]