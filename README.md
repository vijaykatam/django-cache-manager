===============================
django-cache-manager
===============================

Cache manager for django models


[![Build Status])

## Installation

```sh

pip install django-cache-manager
```

## Design


## Usage

```
from django_cache_manager.cache_manager import CacheManager
class MyModel(models.Model):
   
   #set cache manager as default
   objects = CacheManager()

   # or declare a new manager
   cached_objects = CacheManager()
```   

## Development

Use [make](https://www.gnu.org/software/make/) commands to execute development tasks.

* Testing
* Linting
* Creating tgzs and wheels
* ... and more!

To see the full list of commands:

```bash
make
```


## Testing 

To run all tests

```sh
make test
```

To run tests in a specific module
```sh
make test TESTARGS='--tests=tests.some_module_tests'
```
To run tests in a specific test package
```sh
make test TESTARGS='--tests=tests/some_package_tests'
```
To generate a coverage report and run tests for jenkins
```
make coverage
```




