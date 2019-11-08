FROM alpine:3.7

WORKDIR /root
RUN apk add --no-cache --virtual .dev \
	curl \
        gcc \
	gfortran \
        libc-dev \
        make \
        gettext \
  	mercurial \
	ncurses-dev \
    && apk add --no-cache \
        git \
	lua lua-dev luajit-dev\
	python-dev \
	python3-dev \
	ruby ruby-dev \
  	perl-dev \
    && mkdir -p /root/.cache/dein \
    && curl https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh > installer.sh \
    && sh ./installer.sh /root/.cache/dein \
    && git clone https://github.com/vim/vim.git \
    && git clone https://github.com/ryuichi1208/dotfiles \
    && cd vim \
    && ./configure \
        --enable-gui=gtk3 \
        --enable-perlinterp \
        --enable-pythoninterp \
        --enable-python3interp \
        --enable-rubyinterp \
        --enable-luainterp --with-luajit \
        --enable-fail-if-missing \
    && make \
    && make install \
    && apk del --purge .dev \
    && rm -rf /home/vim

COPY --chown=root:root vimrc /root/.vimrc
