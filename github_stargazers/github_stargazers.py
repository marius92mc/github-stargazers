import typing
import click

from halo import Halo

from github_stargazers.github import GitHub
from github_stargazers.github import UsernameRepositoryError, TooManyRequestsHttpError, UrlNotFoundError


class _OutputPrintable(object):
    @staticmethod
    def print_stargazers(stargazers: typing.List[str]) -> None:
        if not stargazers:
            print("0 stargazers.")
            return None
        print("Stargazers:")
        for stargazer in stargazers:
            print(stargazer)

    @staticmethod
    def print_check_stargazer(is_stargazer: bool) -> None:
        return Halo().succeed("Stargazer") if is_stargazer else Halo().fail("Not a Stargazer")


class _Command:  # pylint: disable=too-few-public-methods

    def __init__(self, username_and_repository: str, user: str) -> None:
        self.__username_and_repository: str = username_and_repository
        self.__user: typing.Optional[str] = user

    def __get_github(self) -> typing.Optional[GitHub]:
        try:
            github = GitHub(self.__username_and_repository)
        except (UsernameRepositoryError, UrlNotFoundError) as exception_message:
            Halo().fail(exception_message)
            return None
        return github

    def process(self) -> None:
        github: typing.Optional[GitHub] = self.__get_github()
        if not github:
            return None
        try:
            if self.__user:
                stargazer: bool = github.is_stargazer(self.__user)
                _OutputPrintable.print_check_stargazer(stargazer)
            else:
                stargazers: typing.List[str] = github.get_all_stargazers()
                _OutputPrintable.print_stargazers(stargazers)
        except (TooManyRequestsHttpError, UrlNotFoundError) as exception_message:
            Halo().fail(exception_message)
            return None


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
