FROM python:3.9

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

COPY ./app/.streamlit/config.toml ~/.streamlit/config.toml

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "./Home.py", "--server.port=80", "--server.address=0.0.0.0"]