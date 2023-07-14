# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
#WORKDIR /code
WORKDIR /app
COPY . .

# Set up MySQL dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev default-mysql-client

RUN pip install --no-cache-dir -r requirements.txt

# Expose the Django development server port
EXPOSE 8000

# Run the entrypoint script
#ENTRYPOINT ["entrypoint.sh"]
ENTRYPOINT [ "/bin/bash", "entrypoint.sh"]
