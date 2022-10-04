FROM python:3.10-alpine

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Copy files
COPY app.py /app/
COPY project /app/project
COPY requirements.txt /app/requirements.txt

# Install python packages
RUN pip --disable-pip-version-check --no-cache-dir install -r /app/requirements.txt

# Switch back to dialog
ENV DEBIAN_FRONTEND=dialog

# Start application
ENV FLASK_APP=/app/app.py
CMD [ "flask", "run", "--host=0.0.0.0"]