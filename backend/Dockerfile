FROM python:3.12.4-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install -r hackaton/requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python" ]
CMD [ "hackaton/manage.py", "runserver", "0.0.0.0:8000" ]
