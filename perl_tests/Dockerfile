FROM ubuntu:22.04

# ---------------------------
# 1. Базовые пакеты
# ---------------------------
RUN apt-get update && \
    apt-get install -y \
        perl \
        cpanminus \
        nginx \
        build-essential \
        curl \
        wget \
        libpcre3 \
        libpcre3-dev && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------
# 2. Установка Test::Nginx
# ---------------------------
RUN cpanm --notest Test::Nginx

# ---------------------------
# 3. Каталог с тестами
# ---------------------------
WORKDIR /test

# Копируем весь проект (включая t/, locations-under-test.conf, Dockerfile)
COPY locations-under-test.conf locations-under-test.conf
COPY t/locations_old_query.t t/locations_old_query.t

COPY locations-under-test2.conf locations-under-test2.conf
COPY t/locations_users.t t/locations_users.t

# ---------------------------
# 4. Указываем Test::Nginx, где nginx
# ---------------------------
ENV TEST_NGINX_BINARY=/usr/sbin/nginx

# ---------------------------
# 5. Запуск тестов
# ---------------------------
CMD ["prove", "-I.", "-v", "t/locations_old_query.t"]
#CMD ["prove", "-I.", "-v", "t/locations_users.t"]
