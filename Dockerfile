FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpst-dev \
        pst-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN chmod +x ./extract.sh

# Default command
CMD ["./extract.sh"]
