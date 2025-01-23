FROM python:3.11-slim 

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ENV PORT 5000

COPY . /app/
CMD ["python", "user-id-flask.py"]