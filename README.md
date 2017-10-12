# GitHub Stargazers

List stargazers and check if a user starred that repository

[![Build Status](https://travis-ci.com/marius92mc/github-stargazers.svg?token=NxgJCKyxyV3vmKhB6EpL&branch=master)](https://travis-ci.com/marius92mc/github-stargazers)

## Install 
```
$ pip3 install github-stargazers
```

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
$ pipenv run python src/github_stargazers.py <username>/<repository> [OPTIONS]
```
where `OPTIONS` could be 
```
--user   User name to see if it is a stargazer
```

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

