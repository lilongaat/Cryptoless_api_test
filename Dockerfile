FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Signal handling for PID1 https://github.com/krallin/tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

COPY requirements.txt ./

RUN set -ex \
	&& buildDeps=" \
	build-essential \
	libssl-dev \
	libgmp-dev \
	pkg-config \
	allure \
	autoconf \
	automake \
	libtool \
	git \
	autoconf  \
	" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends $buildDeps \
	&& pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt \
	&& apt-get purge -y --auto-remove $buildDeps \
	&& rm -rf /var/lib/apt/lists/* 

COPY . .
# RUN DJANGO_SETTINGS_MODULE=config.settings.local DJANGOx_DOT_ENV_FILE=.env.local python manage.py collectstatic --noinput

# ENTRYPOINT ["/tini", "--"]
CMD [ "python3"]
