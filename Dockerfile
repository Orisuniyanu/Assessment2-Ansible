FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y python3 python3-pip && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]
