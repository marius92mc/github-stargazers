import typing


def get_examples_invalid_user_repo() -> typing.List[str]:
    return [
        "another_foo/bar",
        "foo/another_bar",
        "another_foo/another_bar"
    ]
