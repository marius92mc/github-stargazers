# pylint: disable=no-member,invalid-name,redefined-outer-name
from click.testing import CliRunner
import pytest
import responses

from github_stargazers.github_stargazers import command_line
from tests import get_examples_invalid_user_repo

@pytest.fixture
def url_page_content() -> str:
    return "<h3>foo</h3> <h3>bar</h3>"


@pytest.fixture
def halo_succeed() -> str:
    return "\r\x1b[K\x1b[32m✔\x1b[39m "


@pytest.fixture
def halo_fail() -> str:
    return "\r\x1b[K\x1b[31m✖\x1b[39m "


@pytest.fixture
def stargazer(halo_succeed: str) -> str:
    return halo_succeed + "Stargazer\n"


@pytest.fixture
def not_a_stargazer(halo_fail: str) -> str:
    return halo_fail + "Not a Stargazer\n"


@pytest.fixture
def wrong_arguments_message(halo_fail: str) -> str:
    return halo_fail + "Argument should be of form username/repository.\n"


@responses.activate
def test_wrong_arguments(wrong_arguments_message: str) -> None:
    wrong_arguments = ["foo", "foo/", "/bar", "/", "//", ""]
    for wrong_argument in wrong_arguments:
        runner = CliRunner()
        result = runner.invoke(command_line, [wrong_argument])
        assert result.exit_code == 0
        assert result.output == wrong_arguments_message


@responses.activate
def test_user_and_repository(url_page_content: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    runner = CliRunner()
    result = runner.invoke(command_line, ['foo/bar'])
    assert result.exit_code == 0
    assert result.output == 'Stargazers:\nbar\nfoo\n'


@pytest.fixture
def http_404(halo_fail: str) -> str:
    return halo_fail +  "404 HTTP.\n"


@pytest.mark.parametrize("invalid_user_and_repo", get_examples_invalid_user_repo())
@responses.activate
def test_get_all_stargazers_on_invalid_user_repo(url_page_content: str,
                                                 invalid_user_and_repo: str,
                                                 http_404: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/" + invalid_user_and_repo + "/stargazers?page=1",
        body=url_page_content,
        status=404)
    runner = CliRunner()
    result = runner.invoke(command_line, [invalid_user_and_repo])
    assert result.exit_code == 0
    assert result.output == http_404


@pytest.fixture
def http_too_many_requests(halo_fail: str) -> str:
    return halo_fail + "Too many requests.\n"


@responses.activate
def test_get_all_stargazers_on_too_many_requests(url_page_content: str,
                                                 http_too_many_requests: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=429)
    runner = CliRunner()
    result = runner.invoke(command_line, ['foo/bar'])
    assert result.exit_code == 0
    assert result.output == http_too_many_requests


@responses.activate
def test_is_stargazer(url_page_content: str, stargazer: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    runner = CliRunner()
    result = runner.invoke(command_line, ['foo/bar', '--user', 'foo'])
    assert result.exit_code == 0
    assert result.output == stargazer


@responses.activate
def test_not_a_stargazer(url_page_content: str, not_a_stargazer: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=200)
    runner = CliRunner()
    result = runner.invoke(command_line, ['foo/bar', '--user', 'another_foo'])
    assert result.exit_code == 0
    assert result.output == not_a_stargazer


@responses.activate
def test_stargazer_on_invalid_page(url_page_content: str, http_404: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=404)
    runner = CliRunner()
    result = runner.invoke(command_line, ['foo/bar', '--user', 'foo'])
    assert result.exit_code == 0
    assert result.output == http_404


@responses.activate
def test_stargazer_on_too_many_requests_page(url_page_content: str, http_too_many_requests: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=429)
    runner = CliRunner()
    result = runner.invoke(command_line, ['foo/bar', '--user', 'foo'])
    assert result.exit_code == 0
    assert result.output == http_too_many_requests
