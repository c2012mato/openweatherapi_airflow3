# Start from the official Airflow image
FROM apache/airflow:3.0.0

# Switch to the root user temporarily to ensure permissions for installing packages
USER root
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && apt-get clean
# Copy .env into the container
COPY .env /opt/airflow/.env


# Switch back to the standard airflow user
USER airflow

#
# THIS IS THE COMMAND THAT INSTALLS YOUR PACKAGES INSIDE THE CONTAINER
#
RUN pip install --no-cache-dir requests pendulum apache-airflow-providers-postgres

# Switch back to the standard airflow user
USER airflow