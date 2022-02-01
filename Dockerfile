FROM python:3

WORKDIR /glimpse
EXPOSE 8000

COPY requirements ./requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD ["./run.sh"]
