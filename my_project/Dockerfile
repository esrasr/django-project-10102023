FROM python:3.9
WORKDIR /code/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY /my_project/requirements.txt /code/
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY /my_project/entrypoint.sh /code/
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY /my_project /code
# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]