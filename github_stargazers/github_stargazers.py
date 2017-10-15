import typing

import click
from halo import Halo

from github_stargazers.github import GitHub
from github_stargazers.github import UsernameRepositoryError, TooManyRequestsHttpError, HTTPError


class _Command:  # pylint: disable=too-few-public-methods

    def __init__(self, username_and_repository: str, user: str) -> None:
        self.__username_and_repository: str = username_and_repository
        self.__user: typing.Optional[str] = user

    def __get_github(self) -> typing.Optional[GitHub]:
        try:
            github = GitHub(self.__username_and_repository)
        except UsernameRepositoryError as exception_message:
            Halo().fail(exception_message)
            return None
        return github

    @classmethod
    def __print_stargazers(cls, github: GitHub) -> None:
        assert github, "github cannot be None"
        try:
            stargazers: typing.List[str] = github.get_all_stargazers()
        except (TooManyRequestsHttpError, HTTPError) as exception_message:
            Halo().fail(exception_message)
            return None
        if not stargazers:
            return None
        print("Stargazers:")
        for stargazer in stargazers:
            print(stargazer)

    def __print_check_stargazer(self, github: GitHub) -> None:
        try:
            stargazer: bool = github.is_stargazer(self.__user)
        except (TooManyRequestsHttpError, HTTPError) as exception_message:
            Halo().fail(exception_message)
            return None
        if stargazer:
            Halo().succeed("Stargazer")
        else:
            Halo().fail("Not a Stargazer")

    def process(self) -> None:
        github: GitHub = self.__get_github()
        if not github:
            return
        if not self.__user:
            _Command.__print_stargazers(github)
        else:
            self.__print_check_stargazer(github)


@click.command()
@click.argument('username_and_repository')
@click.option('--user', default=None, help='User name to see if it is a stargazer')
def command_line(username_and_repository: str, user: str) -> None:
    command = _Command(username_and_repository, user)
    command.process()


def main() -> None:
    command_line()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
