FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Required to install mysqlclient with Pip
RUN apt-get update \
  && apt-get install python3-dev default-libmysqlclient-dev gcc -y


# Install pipenv
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN pip install pipenv

# Install application dependencies
COPY Pipfile Pipfile.lock /app/
# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments.
RUN pipenv install --system --dev

# Copy the application files into the image
COPY . /app/

# Expose port 8000 on the container
EXPOSE 8000