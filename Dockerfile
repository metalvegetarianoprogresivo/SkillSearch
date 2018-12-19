FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

# Install Java
RUN apk update && apk upgrade \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

# Install libraries needed for python lxml library
RUN apk add --no-cache gcc musl-dev libxslt-dev

# Copy Application files
RUN mkdir /skillsearch
COPY . /skillsearch
WORKDIR /skillsearch

# Installing Python dependencies
RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
