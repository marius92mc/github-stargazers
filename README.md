# GitHub Stargazers

[![Build Status](https://travis-ci.org/marius92mc/github-stargazers.svg?branch=master)](https://travis-ci.org/marius92mc/github-stargazers)
[![PyPI version](https://badge.fury.io/py/github-stargazers.svg)](https://badge.fury.io/py/github-stargazers)

List stargazers and check if a user starred that repository.

## Install 
```
$ pip3 install github-stargazers
```

## Usage 
TODO _from installed package_

## Requirements 
- Python 3.6
- [pipenv](https://docs.pipenv.org/)

## Getting started 

1. Install pipenv
```
$ pip3 install pipenv 
```

2. Set Python 3.6 as the version used by pipenv to create the virtual environment
```
$ pipenv --python=python3.6
```

3. Install dependencies 
```
$ pipenv install
```

## Run 
```
$ pipenv run python github_stargazers/github_stargazers.py <username>/<repository> [OPTIONS]
```
where `OPTIONS` could be 
```
--user <username>  User name to see if it is a stargazer, 
                   where username represents the GitHub name. 
```
If it's used without `--user`, it just shows repository's stargazers. 
When it is used with `--user`, it shows if that user starred the repository or not. 

## Run autopep8, mypy, pylint 
```
./autopep8.sh 
./mypy.sh 
./pylint.sh
```

# Launch IPython console 
```
pipenv run ipython
```

## Tests 
Run the unit-tests. 
```
$ pipenv run pytest
```
or with more detailed output, like this `$ pipenv run pytest -vv -s -x`. 

- Debug failing tests 
```
$ pipenv run pytest -vv -x --pdb --showlocals
```
For more details, see the [pytest documentation](https://docs.pytest.org/en/latest/usage.html). 

