# GitHub Stargazers

[![Build Status](https://travis-ci.org/marius92mc/github-stargazers.svg?branch=master)](https://travis-ci.org/marius92mc/github-stargazers)
[![PyPI version](https://badge.fury.io/py/github-stargazers.svg)](https://badge.fury.io/py/github-stargazers)
[![HitCount](http://hits.dwyl.io/marius92mc/github-stargazers.svg)](http://hits.dwyl.io/marius92mc/github-stargazers)
[![tweet](http://jpillora.com/github-twitter-button/img/tweet.png)](https://twitter.com/intent/tweet?text=GitHub+Stargazers+on+PyPi!&url=https%3A%2F%2Fgithub.com%2Fmarius92mc%2Fgithub-stargazers&hashtags=github&original_referer=http%3A%2F%2Fgithub.com%2F&tw_p=tweetbutton)

List stargazers and check if a user starred that repository.

## Install 
It is recommended to be installed in a virtual environment with `Python >= 3.6`.

- Install pipenv
```
$ pip3 install pipenv
```
- After `cd` into a working directory, configure virtual environment and install `github-stargazers`
```
$ pipenv --python=python3.6
$ pipenv install github-stargazers
```

## Usage 

### As a command-line app

```
$ pipenv run github-stargazers <username>/<repository> [OPTIONS]
```
where `OPTIONS` could be
```
--user <username>  User name to see if it is a stargazer. 
                   username represents the GitHub name.
```
If it's used without `--user`, it just shows repository's stargazers.

When it's used with `--user`, it shows if that user starred the repository or not. 

Example: 
```
$ pipenv run github-stargazers marius92mc/github-stargazers 
```

### As an imported

```Python
from github_stargazers.github import GitHub

github = GitHub("yasoob/fb-messenger-bot")

print(github.get_all_stargazers())
print(github.is_stargazer("Robin"))
```

## Running from source

### Requirements 
- Python 3.6
- [pipenv](https://docs.pipenv.org/)

### Getting started 

1. Install pipenv
```
$ pip3 install pipenv 
```

2. Set Python 3.6 as the version used by pipenv to create the virtual environment
```
$ cd github_stargazers
$ pipenv --python=python3.6
```

3. Install dependencies 
```
$ pipenv install --dev
```

### Run 
First we need to install the package, according to `setup.py` instructions.
```
$ pipenv run python setup.py install
```
Then we can run the installed package inside pipenv. 
```
$ pipenv run github-stargazers <username>/<repository> [OPTIONS]
```
where `OPTIONS` could be 
```
--user <username>  User name to see if it is a stargazer, 
                   where username represents the GitHub name. 
```

### Run autopep8, mypy, pylint for the changed files 
```
$ ./autopep8.sh 
$ ./mypy.sh 
$ ./pylint.sh
```

### Launch IPython console 
```
$ pipenv run ipython
```

### Tests 
Run the unit-tests. 
```
$ pipenv run pytest
```
or with more detailed output, like this `$ pipenv run pytest -vv`. 

- Debug failing tests 
```
$ pipenv run pytest -vv -s -x --pdb --showlocals
```
For more details, see the [pytest documentation](https://docs.pytest.org/en/latest/usage.html). 
