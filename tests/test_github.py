# pylint: disable=no-member,invalid-name,redefined-outer-name
import pytest
import responses

from github_stargazers.github import GitHub
from github_stargazers.github import UsernameRepositoryError, TooManyRequestsHttpError, UrlNotFoundError
from github_stargazers.github import MissingHyperlinkTagError, MissingHrefAttributeError, HrefContentError
from tests import get_examples_invalid_user_repo, get_wrong_href_content, get_page_content_with_href


def test_wrong_argument_raises() -> None:
    wrong_arguments = ["foo", "foo/", "/bar", "/", "//", ""]
    for wrong_argument in wrong_arguments:
        with pytest.raises(UsernameRepositoryError):
            GitHub(wrong_argument)


@pytest.fixture
def url_page_content_1() -> str:
    return '<h3> <a href="/foo"> John Williams </a> </h3> ' \
           '<h3> <a href="/bar"> Michael Phelps </a> </h3>'


@pytest.fixture
def url_page_content_2() -> str:
    return '<h3> <a href="/foo2"> John Williams 2 </a> </h3> ' \
           '<h3> <a href="/bar2"> Michael Phelps 2 </a> </h3>'


@responses.activate
def test_get_all_stargazers_has_all_stargazers(url_page_content_1: str,
                                               http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_ok_status_code
    )
    assert set(GitHub("foo/bar").get_all_stargazers()) == set(['foo', 'bar'])


@responses.activate
def test_get_all_stargazers_sorts_stargazers(url_page_content_1: str,
                                             http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_ok_status_code
    )
    assert GitHub("foo/bar").get_all_stargazers() == sorted(['foo', 'bar'])


@pytest.fixture
def url_page_content_without_stargazers() -> str:
    return "<html> <h1> title </h1> </html>"


@responses.activate
def test_get_all_stargazers_returns_empty_on_page_without_stargazers(url_page_content_without_stargazers: str,
                                                                     http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_without_stargazers,
        status=http_ok_status_code
    )
    assert GitHub("foo/bar").get_all_stargazers() == []


@responses.activate
def test_get_all_stargazers_sorts_stargazers_two_pages(url_page_content_1: str,
                                                       url_page_content_2: str,
                                                       http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_ok_status_code
    )
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=2",
        body=url_page_content_2,
        status=http_ok_status_code
    )
    assert GitHub("foo/bar").get_all_stargazers() == sorted(['foo', 'bar', 'foo2', 'bar2'])


@pytest.mark.parametrize("invalid_user_and_repo", get_examples_invalid_user_repo())
@responses.activate
def test_get_all_stargazers_on_invalid_user_repo_raises(url_page_content_1: str,
                                                        invalid_user_and_repo: str,
                                                        http_not_found_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/" + invalid_user_and_repo + "/stargazers?page=1",
        body=url_page_content_1,
        status=http_not_found_status_code
    )
    with pytest.raises(UrlNotFoundError):
        GitHub(invalid_user_and_repo).get_all_stargazers()


@responses.activate
def test_get_all_stargazers_on_too_many_requests_raises(url_page_content_1: str,
                                                        http_too_many_requests_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_too_many_requests_status_code
    )
    with pytest.raises(TooManyRequestsHttpError):
        GitHub("foo/bar").get_all_stargazers()


@responses.activate
def test_provided_user_is_stargazer(url_page_content_1: str, http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_ok_status_code
    )
    assert GitHub("foo/bar").is_stargazer("foo")


@responses.activate
def test_provided_user_is_stargazer_on_last_page(url_page_content_1: str,
                                                 url_page_content_2: str,
                                                 http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_ok_status_code
    )
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=2",
        body=url_page_content_2,
        status=http_ok_status_code
    )
    assert GitHub("foo/bar").is_stargazer("bar2")


@responses.activate
def test_provided_user_is_not_stargazer(url_page_content_1: str, http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_ok_status_code
    )
    assert not GitHub("foo/bar").is_stargazer("another_foo")


@responses.activate
def test_provided_user_is_not_stargazer_on_page_without_stargazers(url_page_content_without_stargazers: str,
                                                                   http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_without_stargazers,
        status=http_ok_status_code
    )
    assert not GitHub("foo/bar").is_stargazer("another_foo")


@responses.activate
def test_provided_user_on_invalid_page(url_page_content_1: str, http_not_found_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_not_found_status_code
    )
    with pytest.raises(UrlNotFoundError):
        GitHub("foo/bar").is_stargazer("foo")


@responses.activate
def test_provided_user_on_too_many_requests_page(url_page_content_1: str,
                                                 http_too_many_requests_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=http_too_many_requests_status_code
    )
    with pytest.raises(TooManyRequestsHttpError):
        GitHub("foo/bar").is_stargazer("foo")


@responses.activate
def test_provided_user_with_missing_hyperlink_tag(url_page_content_missing_hyperlink_tag: str,
                                                  http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_missing_hyperlink_tag,
        status=http_ok_status_code
    )
    with pytest.raises(MissingHyperlinkTagError):
        GitHub("foo/bar").is_stargazer("foo")


@responses.activate
def test_provided_user_with_missing_href_attribute(url_page_content_missing_href_attribute: str,
                                                   http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_missing_href_attribute,
        status=http_ok_status_code
    )
    with pytest.raises(MissingHrefAttributeError):
        GitHub("foo/bar").is_stargazer("foo")


@pytest.mark.parametrize("wrong_href_content", get_wrong_href_content())
@responses.activate
def test_wrong_href_content_raises(wrong_href_content: str,
                                   http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=get_page_content_with_href(wrong_href_content),
        status=http_ok_status_code
    )
    with pytest.raises(HrefContentError):
        GitHub("foo/bar").is_stargazer("foo")
