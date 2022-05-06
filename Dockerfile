FROM python:3.9.6

LABEL version="1.0"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /

COPY . . 

RUN pip install --upgrade pip
RUN pip install -r requirements/req.dev.txt
RUN pip install debugpy

EXPOSE 3001

CMD ["sh", "-c", "python -m debugpy --listen 0.0.0.0:5678 app.py"]