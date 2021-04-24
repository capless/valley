FROM capless/capless-docker:jupyter
COPY . /code
RUN poetry install
