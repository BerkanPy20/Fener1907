FROM python:3.11-slim-trixie

WORKDIR /app

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates sqlite3 libsqlite3-dev && apt-get clean

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1


COPY ./Session_5/chatbot_task/ /app/
COPY pyproject.toml /app/
COPY .python-version /app/
COPY uv.lock /app/


RUN uv sync --locked

# Expose the application port
EXPOSE 5001 5678

# Run python debug server and streamlit with live reload enabled
CMD ["uv", "run", "streamlit", "run", "./app/main.py", "--server.port=5001", "--server.address=0.0.0.0"]
