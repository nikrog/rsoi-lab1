FROM python:3
WORKDIR /code
COPY . /code/

# install our dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["sh", "entrypoint.sh"]