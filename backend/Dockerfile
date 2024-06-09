FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY . /app

RUN ls
RUN pip install -r hackaton/requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python" ]
CMD [ "hackaton/manage.py", "runserver" ]