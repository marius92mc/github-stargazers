import typing


def get_examples_invalid_user_repo() -> typing.List[str]:
    return [
        "another_foo/bar",
        "foo/another_bar",
        "another_foo/another_bar"
    ]


def get_wrong_href_content() -> typing.List[str]:
    return ["/", "a", "baz"]


def get_page_content_with_href(href: str) -> str:
    return '<h3> <a href="' + href + '"> John Williams </a> </h3>'
