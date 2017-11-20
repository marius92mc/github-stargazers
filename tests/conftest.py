import pytest


@pytest.fixture
def ok_status_code() -> int:
    return 200


@pytest.fixture
def too_many_requests_status_code() -> int:
    return 429


@pytest.fixture
def not_found_status_code() -> int:
    return 404


@pytest.fixture
def url_page_content_no_hyperlink() -> str:
    return '<h3> foo </h3>'


@pytest.fixture
def url_page_content_no_href() -> str:
    return '<h3> <a> John Williams </a> </h3>'
