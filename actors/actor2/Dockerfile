FROM python:3.10-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY script.py script.py
CMD ["python3", "./script.py"]
