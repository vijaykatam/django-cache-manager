History
-------

0.1.5
---------------------
* [BUGFIX] - Fix for non-ascii characters in query.


0.1.4
---------------------
* [BUGFIX] - Fix cache eviction on bulk updates for models that have a ManyToManyField with an intermediate(through) model.


0.1.3
---------------------
* [BUGFIX] - Fix cache eviction for models that have a ManyToManyField with an intermediate(through) model.


0.1.2
---------------------
* [BUGFIX] - Properly handle passing of an empty iterable to '__in' filter args.  Related Django bug: https://code.djangoproject.com/ticket/12717


0.1.1
---------------------

* [BUGFIX] - Invalidate related model caches for changes, needed for select_related queries.


0.1.0
---------------------

* Test coverage
* Cache invalidation for manytomany relation


0.1.0-beta.1
---------------------

* First beta release
