FROM python:3.10-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY http_script.py http_script.py
CMD ["python3", "./http_script.py"]
