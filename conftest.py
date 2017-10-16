import typing
import pytest 


@pytest.fixture
def http_ok_status_code() -> int:
    return 200


@pytest.fixture
def http_too_many_requests_status_code() -> int:
    return 429


@pytest.fixture
def http_not_found_status_code() -> int:
    return 404

