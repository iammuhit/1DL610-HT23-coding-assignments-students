# Base Image
FROM python:latest

LABEL maintainer="Nurul Amin Muhit <me@muhit.me>"
LABEL description="Software Testing Assignment"
LABEL version="1.0.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Prerequisites
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

# Set Working Directory
WORKDIR /usr/src

# Copy Application
COPY requirements.txt /usr/src
COPY . /usr/src

# Install Dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
