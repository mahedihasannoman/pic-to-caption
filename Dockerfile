FROM python:3.10-slim

ARG USERNAME=mahedi
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# System dependencies
RUN apt-get update && apt-get install -y git libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy files
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

USER $USERNAME

# Run API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
