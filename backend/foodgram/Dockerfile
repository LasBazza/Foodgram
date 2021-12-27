FROM python:3.7

WORKDIR /myproject

COPY ./backend/requirements.txt .

RUN pip install -r requirements.txt

COPY ./backend/foodgram ./backend/script.sh ./data/ingredients.json ./

RUN chmod +x /myproject/script.sh

ENTRYPOINT ["/myproject/script.sh"]