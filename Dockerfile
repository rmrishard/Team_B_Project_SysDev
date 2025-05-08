FROM python:3.13-bookworm
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./backend /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "5000"]