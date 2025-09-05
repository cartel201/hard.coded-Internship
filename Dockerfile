# Python image
FROM python:3.11-slim

#  environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#  work directory
WORKDIR /app

#  dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# project files
COPY . /app/

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
