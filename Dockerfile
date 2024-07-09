FROM python:3.12 

RUN mkdir /app 

WORKDIR /app 

COPY req.txt .

RUN pip inrtall -r req.txt

COPY . .

WORKDIR src 

CMD guvicorn