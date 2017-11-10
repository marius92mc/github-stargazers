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


@pytest.fixture
def url_page_content_missing_hyperlink_tag() -> str:
    return '<h3> foo </h3>'


@pytest.fixture
def url_page_content_missing_href_attribute() -> str:
    return '<h3> <a> John Williams </a> </h3>'
