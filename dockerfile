#Python base image
FROM python:3.10-slim

#set working dir
WORKDIR /app

#copy current dir to working dir
COPY . /app

#upgrade pip
RUN pip install --upgrade pip

#install packages from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

#run the API using django dev servers
CMD ["python", "stbcApi/manage.py", "runserver", "0.0.0.0:8000"]