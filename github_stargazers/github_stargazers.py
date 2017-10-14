import typing

import click
from halo import Halo

from github import GitHub
from github import UsernameRepositoryError


@click.command()
@click.argument('username_and_repository')
@click.option('--user', default=None, help='User name to see if it is a stargazer')
def process_command(username_and_repository, user):
    try:
        github = GitHub(username_and_repository)
    except UsernameRepositoryError:
        message = "Wrong arguments. It should be of form username/repository, e.g. marius92mc/github-stargazers"
        Halo().fail(message)
        return
    if not user:
        stargazers: typing.List[str] = github.get_all_stargazers()
        print("Stargazers: ")
        for stargazer in stargazers:
            print(stargazer)
        return

    if github.is_stargazer(user):
        Halo().succeed("Stargazer")
    else:
        Halo().fail("Not a Stargazer")


def main():
    process_command()  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    main()
