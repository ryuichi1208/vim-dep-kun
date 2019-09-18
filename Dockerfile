FROM alpine:3.7
RUN apk add --no-cache --virtual .build \
        git \
        gcc \
        libc-dev \
        make \
        gettext \
        ncurses-dev \
