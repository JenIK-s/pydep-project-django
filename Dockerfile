FROM python:3.10.9-slim
WORKDIR /app
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip --no-cache-dir
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY ./pydep /app
CMD ["gunicorn", "pydep.wsgi:application", "--bind", "0.0.0.0:8000" ]