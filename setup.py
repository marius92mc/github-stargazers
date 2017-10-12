# pylint: disable=no-name-in-module,import-error
from setuptools import setup


setup(
    name='github-stargazers',
    #package_dir = {'': 'github-stargazers'},
    packages=['github_stargazers'],
    version='0.0.2',
    description='List stargazers and check if a user starred that repository',
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
