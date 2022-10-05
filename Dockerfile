FROM python:3.8-alpine

ADD email_api.py .

ADD requirments.txt .

RUN pip install -r requirments.txt

CMD ["python" , "./email_api.py"]