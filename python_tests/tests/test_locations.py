import requests, yaml, time

BASE = "http://localhost:8080"

def _get_with_retry(path, retries=30, delay=0.2):
    last_exc = None
    for _ in range(retries):
        try:
            return requests.get(BASE + path, timeout=2)
        except Exception as e:
            last_exc = e
            time.sleep(delay)
    raise last_exc

def _h(headers, key):
    # case-insensitive доступ к заголовкам эхо-сервиса
    key = key.lower()
    for k, v in headers.items():
        if k.lower() == key:
            return v
    return None

def load_cases():
    with open("tests/cases.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_locations_table():
    for case in load_cases():
        inp = case["in"]
        expected = case["out"]

        r = _get_with_retry(inp)
        assert r.status_code == 200, f"{inp}: unexpected status {r.status_code}"
        payload = r.json()

        # 1) Что увидел апстрим (реальный итог переписывания)
        assert payload["path"] == expected, f"{inp} -> {payload['path']} != {expected}"

        # 2) Диагностика: проверим, что мы НЕ шлём в апстрим исходный request_uri
        x_orig = _h(payload["headers"], "X-Orig-Request-URI")
        assert x_orig == inp, f"{inp}: X-Orig-Request-URI должен быть исходным"

        # 3) Дополнительно: nginx-овский $uri действительно изменён, если ожидался rewrite
        x_uri = _h(payload["headers"], "X-Uri")
        # Если ожидаемое отличается от входа (без домена), то и $uri должен отличаться по пути (без query)
        if expected.split("?",1)[0] != inp.split("?",1)[0]:
            assert x_uri == expected.split("?",1)[0], f"{inp}: $uri должен быть {expected.split('?',1)[0]}, а не {x_uri}"


print("зннннннннн")