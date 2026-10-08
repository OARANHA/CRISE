"""Regression tests for login and API IP trust boundaries."""

import pytest
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, override_settings

from apps.accounts.middleware import AuthRateLimitMiddleware
from apps.api.limits import _client_ip


@pytest.mark.parametrize(
    ("peer", "forwarded", "trusted", "expected"),
    [
        ("198.51.100.3", "203.0.113.5", (), "198.51.100.3"),
        ("198.51.100.3", "203.0.113.5", ("192.0.2.1",), "198.51.100.3"),
        ("192.0.2.1", "198.51.100.10, 203.0.113.15", ("192.0.2.1",), "203.0.113.15"),
        ("192.0.2.1", "203.0.113.15, 192.0.2.2", ("192.0.2.1", "192.0.2.2"), "203.0.113.15"),
        ("192.0.2.1", "192.0.2.2, 192.0.2.1", ("192.0.2.1", "192.0.2.2"), "192.0.2.1"),
        ("192.0.2.1", "not-an-ip, 203.0.113.15", ("192.0.2.1",), "203.0.113.15"),
        ("192.0.2.1", "198.51.100.1, invalid", ("192.0.2.1",), "192.0.2.1"),
        ("192.0.2.1", ", 203.0.113.15", ("192.0.2.1",), "192.0.2.1"),
        ("192.0.2.1", "2001:db8::10", ("192.0.2.1",), "2001:db8::10"),
    ],
)
def test_ip_resolution_requires_trusted_proxy(peer, forwarded, trusted, expected):
    with override_settings(BB_TRUSTED_PROXIES=trusted):
        req = RequestFactory().post(
            "/accounts/login/",
            REMOTE_ADDR=peer,
            HTTP_X_FORWARDED_FOR=forwarded,
        )
        assert _client_ip(req) == expected
        assert AuthRateLimitMiddleware._get_client_ip(req) == expected


def test_login_throttle_cannot_be_bypassed_by_forging_first_xff_hop():
    cache.clear()
    middleware = AuthRateLimitMiddleware(lambda _req: HttpResponse("accepted"))
    try:
        with override_settings(BB_TRUSTED_PROXIES=("192.0.2.1",)):
            for i in range(10):
                req = RequestFactory().post(
                    "/accounts/login/",
                    REMOTE_ADDR="192.0.2.1",
                    HTTP_X_FORWARDED_FOR=f"198.51.100.{i + 1}, 203.0.113.10",
                )
                assert middleware(req).status_code == 200
            bypass = RequestFactory().post(
                "/accounts/login/",
                REMOTE_ADDR="192.0.2.1",
                HTTP_X_FORWARDED_FOR="198.51.100.250, 203.0.113.10",
            )
            assert middleware(bypass).status_code == 429
    finally:
        cache.clear()


def test_direct_login_throttle_ignores_forwarded_header():
    cache.clear()
    middleware = AuthRateLimitMiddleware(lambda _req: HttpResponse("accepted"))
    try:
        with override_settings(BB_TRUSTED_PROXIES=()):
            for i in range(10):
                req = RequestFactory().post(
                    "/accounts/login/",
                    REMOTE_ADDR="198.51.100.99",
                    HTTP_X_FORWARDED_FOR=f"203.0.113.{i + 1}",
                )
                assert middleware(req).status_code == 200
            req = RequestFactory().post("/accounts/login/", REMOTE_ADDR="198.51.100.99")
            assert middleware(req).status_code == 429
    finally:
        cache.clear()
