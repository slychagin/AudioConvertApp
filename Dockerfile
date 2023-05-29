FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /audio_convert_app

WORKDIR /audio_convert_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' ./entrypoint.sh && \
    chmod +x  ./entrypoint.sh && \
    apt-get update && \
    apt-get install ffmpeg -y

ENTRYPOINT ["./entrypoint.sh"]