# pylint: disable=no-member,invalid-name,redefined-outer-name
from click.testing import CliRunner
from click.testing import Result
import pytest
import responses

from github_stargazers.github_stargazers import command_line
from tests import get_examples_invalid_user_repo


@pytest.fixture
def url_page_content() -> str:
    return '<h3> <a href="/foo"> John Williams </a> </h3> ' \
           '<h3> <a href="/bar"> Michael Phelps </a> </h3>'


@pytest.fixture
def url_page_content_without_stargazers() -> str:
    return "<html> <h1> title </h1> </html>"


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


def verify_invoke_from_clirunner(result: Result, expected_output: str) -> None:
    assert result.exit_code == 0
    assert result.output == expected_output


@responses.activate
def test_wrong_arguments(wrong_arguments_message: str) -> None:
    wrong_arguments = ["foo", "foo/", "/bar", "/", "//", ""]
    for wrong_argument in wrong_arguments:
        result = CliRunner().invoke(command_line, [wrong_argument])
        verify_invoke_from_clirunner(result, wrong_arguments_message)


@responses.activate
def test_user_and_repository_shows_sorted_stargazers(url_page_content: str,
                                                     http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=http_ok_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar'])
    verify_invoke_from_clirunner(result, 'Stargazers:\nbar\nfoo\n')


@responses.activate
def test_get_all_stargazers_shows_message_on_page_without_stargazers(url_page_content_without_stargazers: str,
                                                                     http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/baz/stargazers?page=1",
        body=url_page_content_without_stargazers,
        status=http_ok_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/baz'])
    verify_invoke_from_clirunner(result, "0 stargazers.\n")


def http_not_found(repository: str) -> str:
    return halo_fail() + "Resource not Found. Check that the repository " + repository + " is correct.\n"


@pytest.mark.parametrize("invalid_user_and_repo", get_examples_invalid_user_repo())
@responses.activate
def test_get_all_stargazers_on_invalid_user_repo(url_page_content: str,
                                                 invalid_user_and_repo: str,
                                                 http_not_found_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/" + invalid_user_and_repo + "/stargazers?page=1",
        body=url_page_content,
        status=http_not_found_status_code
    )

    result = CliRunner().invoke(command_line, [invalid_user_and_repo])
    verify_invoke_from_clirunner(result, http_not_found(invalid_user_and_repo))


@pytest.fixture
def http_too_many_requests(halo_fail: str) -> str:
    return halo_fail + "Too many requests.\n"


@responses.activate
def test_get_all_stargazers_on_too_many_requests(url_page_content: str,
                                                 http_too_many_requests_status_code: int,
                                                 http_too_many_requests: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=http_too_many_requests_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar'])
    verify_invoke_from_clirunner(result, http_too_many_requests)


@responses.activate
def test_is_stargazer(url_page_content: str,
                      stargazer: str,
                      http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=http_ok_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar', '--user', 'foo'])
    verify_invoke_from_clirunner(result, stargazer)


@responses.activate
def test_not_a_stargazer(url_page_content: str,
                         not_a_stargazer: str,
                         http_ok_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=http_ok_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar', '--user', 'another_foo'])
    verify_invoke_from_clirunner(result, not_a_stargazer)


@responses.activate
def test_stargazer_on_invalid_page(url_page_content: str,
                                   http_not_found_status_code: int) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=http_not_found_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar', '--user', 'foo'])
    verify_invoke_from_clirunner(result, http_not_found("foo/bar"))


@responses.activate
def test_stargazer_on_too_many_requests_page(url_page_content: str,
                                             http_too_many_requests_status_code: int,
                                             http_too_many_requests: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content,
        status=http_too_many_requests_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar', '--user', 'foo'])
    verify_invoke_from_clirunner(result, http_too_many_requests)


@pytest.fixture
def missing_hyperlink_tag(halo_fail: str) -> str:
    return halo_fail + "Missing hyperlink tag.\n"


@responses.activate
def test_stargazer_on_missing_hyperlink_tag(url_page_content_missing_hyperlink_tag: str,
                                            http_ok_status_code: int,
                                            missing_hyperlink_tag: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_missing_hyperlink_tag,
        status=http_ok_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar', '--user', 'foo'])
    verify_invoke_from_clirunner(result, missing_hyperlink_tag)


@pytest.fixture
def missing_href_attribute(halo_fail: str) -> str:
    return halo_fail + "Missing 'href' attribute from hyperlink tag.\n"


@responses.activate
def test_stargazer_on_missing_href_attribute(url_page_content_missing_href_attribute: str,
                                             http_ok_status_code: int,
                                             missing_href_attribute: str) -> None:
    responses.add(
        responses.GET,
        "https://github.com/foo/bar/stargazers?page=1",
        body=url_page_content_missing_href_attribute,
        status=http_ok_status_code
    )
    result = CliRunner().invoke(command_line, ['foo/bar', '--user', 'foo'])
    verify_invoke_from_clirunner(result, missing_href_attribute)
