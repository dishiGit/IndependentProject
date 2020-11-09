FROM python:3.6-alpine
RUN adduser -D myproj
WORKDIR /home/myproj
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/api.py ./
RUN chown -R myproj:myproj ./
USER myproj
CMD uvicorn api:app --host 0.0.0.0 --port 5000