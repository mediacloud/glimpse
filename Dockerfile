FROM python:3

WORKDIR /glimpse
EXPOSE 8000

RUN pip install spacy
RUN python -m spacy download en_core_web_sm

COPY requirements ./requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD ["./run.sh"]
