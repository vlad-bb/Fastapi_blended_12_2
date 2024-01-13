FROM python:3.11

ENV ASSISTANT /bot
WORKDIR $ASSISTANT
COPY . .
RUN pip install pipenv
RUN pipenv install --system --deploy
EXPOSE 7777
ENTRYPOINT ["python", "__main__.py"]