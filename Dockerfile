FROM python:3.10-alpine3.17

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache blender-headless && \
    ln -s /usr/bin/blender-headless /usr/bin/blender

RUN apk add --no-cache mesa-gl mesa-egl mesa-gles mesa-dri-gallium

WORKDIR  /app

RUN pip3 install --upgrade pip && \
    pip3 install gunicorn flask

COPY . .


CMD ["gunicorn", "-w", "2", "server:app", "--bind", "0.0.0.0:7860"]
