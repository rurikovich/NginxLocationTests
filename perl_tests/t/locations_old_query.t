use warnings;
use Test::Nginx::Socket -Base;
plan tests => repeat_each()*2;
no_shuffle();
run_tests();
__DATA__
=== TEST 1: rewrite + proxy + заголовки (обычный путь с сегментами)
--- http_config
    server {
        listen 1984;
        location / {
            return 200 "$request_uri\n$http_x_orig_request_uri\n$http_x_uri\n$http_host\n";
        }
    }
--- config
    set $MY_SERVER http://127.0.0.1:1984;
    include /test/locations-under-test.conf;
    listen 127.0.0.1:8080;
    server_name test.local;
--- request
GET /api/v1/old-query/42
--- more_headers
Host: example.test
--- response_body_like: ^\/api.*$
--- error_code: 200
