
FROM python:3.13.6-slim

WORKDIR /usr/src/app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

RUN apt-get update && apt-get install -y sqlite3

# Copy the source code into the container.
COPY . .

# Set appuser as the owner of the app folder (apparently folder ownership required for db write)
# Probably should have the db file in a subfolder for the permissions to make sense
RUN chown appuser:appuser /usr/src/app

# Switch to the non-privileged user to run the application.
USER appuser

RUN touch ./database.db

RUN sqlite3 database.db < schema.sql && sqlite3 database.db < init.sql && sqlite3 database.db < indices.sql

# Set appuser as the owner of the database file. This makes writing possible
# RUN chown appuser:appuser database.db

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD ["flask", "run", "-h", "0.0.0.0"]
