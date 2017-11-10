# pylint: disable=no-name-in-module,import-error
from os import path
from setuptools import setup


def get_version():
    return '0.0.5'


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
    entry_points={
        'console_scripts': [
            'github-stargazers=github_stargazers.github_stargazers:command_line'
        ]
    },
    install_requires=[
        'beautifulsoup4>=4.6.0',
        'halo>=0.0.7',
        'click>=6.7',
        'requests>=2.18.4'
    ],
    version=get_version(),
    description='List stargazers and check if a user starred that repository',
    long_description=get_long_description(),
    author='Marius-Constantin Melemciuc',
    author_email='mariuspypi@gmail.com',
    url='https://github.com/marius92mc/github-stargazers',
    download_url='https://github.com/' +
    'marius92mc/github-stargazers/archive/' + get_version() + '.tar.gz',
    keywords=[
        'command-line',
        'python',
        'github',
        'star',
        'repository',
        'beautifulsoup'],
    classifiers=[],
)
