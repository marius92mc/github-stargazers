# pylint: disable=no-member,invalid-name,redefined-outer-name
import pytest
import responses

from src.github_stargazers import GitHub
from src.github_stargazers import UsernameRepositoryError


def test_wrong_argument_raises() -> None:
    wrong_arguments = ["foo", "foo/", "/bar", "/", "//", ""]
    for wrong_argument in wrong_arguments:
        with pytest.raises(UsernameRepositoryError):
            GitHub(wrong_argument)


@pytest.fixture
def url_page_content() -> str:
    return "<h3>foo</h3> <h3>bar</h3>"


@responses.activate
def test_get_all_stargazers_has_all_stargazers(url_page_content: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    assert set(GitHub("foo/bar").get_all_stargazers()) == set(['foo', 'bar'])


@responses.activate
def test_get_all_stargazers_sorts_stargazers(url_page_content: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    assert GitHub("foo/bar").get_all_stargazers() == sorted(['foo', 'bar'])


@responses.activate
def test_provided_user_is_stargazer(url_page_content: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    assert GitHub("foo/bar").is_stargazer("foo")


@responses.activate
def test_provided_user_is_not_stargazer(url_page_content: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    assert not GitHub("foo/bar").is_stargazer("another_foo")
