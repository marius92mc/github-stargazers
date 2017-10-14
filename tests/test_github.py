# pylint: disable=no-member,invalid-name,redefined-outer-name
import pytest
import responses

from github_stargazers.github import GitHub
from github_stargazers.github import UsernameRepositoryError


def test_wrong_argument_raises() -> None:
    wrong_arguments = ["foo", "foo/", "/bar", "/", "//", ""]
    for wrong_argument in wrong_arguments:
        with pytest.raises(UsernameRepositoryError):
            GitHub(wrong_argument)


@pytest.fixture
def url_page_content_1() -> str:
    return "<h3>foo</h3> <h3>bar</h3>"


@pytest.fixture
def url_page_content_2() -> str:
    return "<h3>foo2</h3> <h3>bar2</h3>"


@responses.activate
def test_get_all_stargazers_has_all_stargazers(url_page_content_1: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=200)
    assert set(GitHub("foo/bar").get_all_stargazers()) == set(['foo', 'bar'])


@responses.activate
def test_get_all_stargazers_sorts_stargazers(url_page_content_1: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=200)
    assert GitHub("foo/bar").get_all_stargazers() == sorted(['foo', 'bar'])


@pytest.fixture
def url_page_content_without_stargazers() -> str:
    return "<html> <h1> title </h1> </html>"


@responses.activate
def test_get_all_stargazers_returns_empty_on_page_without_stargazers(url_page_content_without_stargazers: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_without_stargazers,
        status=200)
    assert GitHub("foo/bar").get_all_stargazers() == []


@responses.activate
def test_get_all_stargazers_sorts_stargazers_two_pages(url_page_content_1: str,
                                                       url_page_content_2: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=200)
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=2",
        body=url_page_content_2,
        status=200)
    assert GitHub("foo/bar").get_all_stargazers() == sorted(['foo', 'bar', 'foo2', 'bar2'])


@responses.activate
def test_provided_user_is_stargazer(url_page_content_1: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=200)
    assert GitHub("foo/bar").is_stargazer("foo")


@responses.activate
def test_provided_user_is_stargazer_on_last_page(url_page_content_1: str,
                                                 url_page_content_2: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=200)
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=2",
        body=url_page_content_2,
        status=200)
    assert GitHub("foo/bar").is_stargazer("bar2")


@responses.activate
def test_provided_user_is_not_stargazer(url_page_content_1: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_1,
        status=200)
    assert not GitHub("foo/bar").is_stargazer("another_foo")

@responses.activate
def test_provided_user_is_not_stargazer_on_page_without_stargazers(url_page_content_without_stargazers: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_without_stargazers,
        status=200)
    assert not GitHub("foo/bar").is_stargazer("another_foo")
