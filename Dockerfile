FROM capless/capless-docker:jupyter
COPY . /code
RUN pip install --upgrade poetry
RUN poetry install
