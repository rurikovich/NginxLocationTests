# t/users_rewrite.t
use Test::Nginx::Socket -Base;

plan tests => 2;

run_tests();

__DATA__

=== TEST 1: rewrite /api/users -> /internal/users and proxy headers
--- http_config
    # Фейковый upstream, чтобы было куда проксировать
    upstream users_backend {
        server 127.0.0.1:1984;
    }

    # Бэкенд-сервер, который просто возвращает uri и заголовки
    server {
        listen 1984;
        location / {
            return 200 "$uri\n$http_x_orig_request_uri\n$http_x_uri\n";
        }
    }

--- config
    # В бою у тебя это set $users_server ${USERS_SERVER};
    # Здесь для простоты задаём напрямую
    set $users_server http://users_backend;

    # Аналог INTERNAL_USERS_PREFIX
    set $internal_users_prefix /internal/users;

    location /api/users {
      rewrite /api/users/(.*) $internal_users_prefix/$1 break;
      proxy_set_header Host $host;
      proxy_set_header X-Orig-Request-URI $request_uri;
      proxy_set_header X-Uri $uri;
      proxy_pass $users_server;
    }

--- request
GET /api/users/123/profile
--- more_headers
Host: example.test
--- error_code: 200
--- response_body_like
^/internal/users/123/profile\n/api/users/123/profile\n/internal/users/123/profile\n$
