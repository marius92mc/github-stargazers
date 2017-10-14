# pylint: disable=no-name-in-module,import-error
from os import path
from setuptools import setup


def get_long_description():
    try:
        import pypandoc
        long_description = pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        long_description = open('README.md').read()
    return long_description


setup(
    name='github-stargazers',
    #package_dir = {'': 'github-stargazers'},
    packages=['github_stargazers'],
    version='0.0.3',
    description='List stargazers and check if a user starred that repository',
    long_description=get_long_description(),
    author='Marius-Constantin Melemciuc',
    author_email='mariuspypi@gmail.com',
    url='https://github.com/marius92mc/github-stargazers',
    download_url='https://github.com/' +
    'marius92mc/github-stargazers/archive/0.0.1.tar.gz',
    keywords=[
        'command-line',
        'python',
        'github',
        'star',
        'repository',
        'beautifulsoup'],
    classifiers=[],
)
