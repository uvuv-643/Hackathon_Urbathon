FROM tiangolo/uwsgi-nginx:python3.11
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./poetry.lock /var/www/app/poetry.lock
COPY ./pyproject.toml /var/www/app/pyproject.toml
COPY ./README.md /var/www/app/README.md
COPY ./urbaton /var/www/app/urbaton
RUN apt-get update \
    && apt-get install libsm6 libxext6  -y  \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/*



RUN pip install poetry
ENV PATH="${PATH}:~/.local/bin"
RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev  --directory /var/www/app