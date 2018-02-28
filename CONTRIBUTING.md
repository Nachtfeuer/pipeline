# How to contribute

The guideline is a living document which is expected to be updated for details which
are focusing on software development and how people should work together. Contribution
is highly appreciated.

## Code of conduct

It is expected the everybody working on this project is following the rules as
defined in [Code Of Conduct](CODE_OF_CONDUCT.md). Please report unaccepted behavior
to thomas.lehmann.private@gmail.com.


## Design

- Always keep in mind that a tool (like spline) is intended to be useful.
- Please keep things simple.
- Think about how you can hide complexity for the user of the tool.
- The tool should also support the user to detect issues more easily.
- The main idea (not always possible, that's clear): just to have one yaml file for all with no external dependencies.

## Keeping and improving quality

There are many criteria for quality and many of them can be verified by tools. So please
verify before each commit of your changes that the quality is fine:

 - use `tox -e py27` (it runs all checks). You also can use a Python 3.x (see tox.ini).
   Sometimes running both make sense. Travis CI anyway will find out for each Python version that is
   supported but checking locally first can reduce a lot of pain.
 - in general keep code readable, avoid too complex code, keep units (methods, functions, files)
   as small as possible, use readable names and provide code documentation.
 - tools like pylint, pep8 (or pycodestyle), pep257, flake8, radon and bandit are your friends.
   don't do tricks otherwise you trick yourself. There are exceptions where you can disable a
   warning but please don't overdo. One good example is `no-self-use` in unittests which make
   sense to be disabled.
 - always use an issue (ticket) that you can refer to when writing the commit message so that the issue and
   the code are linked together.
 - For all changes please keep the documentation up-to-date. There is the documentation (*.rst) which
   can be seen on read the docs as well as the **spline.rst** for the PyPI and the **README.md** which
   will be seen when visiting the project on Github.

## Python versions

- Of course newer Python version might introduce syntax sugar but the focus should be here to support as many
  Python versions as possible. For the moment Python 2.7.x is the one and only Python 2 version supported by spline.
  Also PyPy is supported.
- The author of spline does observe on what's provided by current Debian version and and current CentOS version.
- Please consider to use the **pipeline.yaml** to run tests (also the ones for Docker are disabled then) for Python
  versions you do not have on your system.
- When a new Python version can be added please update the **pipeline.yaml** as well as the **.travis.yml**.


## Version policy

 - The standard spline version follows the rule `<major>.<minor>`.
 - The project is organized via milestones using this version policy.
 - The major version is a strategic increment: one day when it seems that all added functionality
   should represent a new major version the increment should be done.
 - Usually each milestone the minor version is incremented once.
 - Bugfixes should be represented as `<major>.<minor>.<bugfix>` and the bugfix should start with 1.
 - The bugfix number should vanish on a new milestone.

## Tags and branches

  - A milestone is a feature branch with name `milestone-<major>.<minor>`
    branched out from git master.
  - For a bugfix a branch `milestone-<major>.<minor>-fix-<bugfix>` should be created from the last
    tag (version) that has been published on PyPI.
  - A tag is created when a milestone branch or bugfix branch has been merged to git master

## Pull requests
  - Branch protection is adjusted to disable direct push on git master. Also the author of spline
    can merge directly it is a very very very rare case where this is used. Please always use
    pull requests. The build and coveralls.io (at least) tell you whether all seems fine.
  - When merging a milestone (normal usecase) then please keep the branch (very old branches - when
    there are really a lot of them - can be removed).

## Milestones

  - When a milestone is completed (merged) then please tag git master with the latest version.
  - After that create a wheel package (`tox -e package`) and upload it to PyPI with **twine**.
    At the moment the author of spline does have the account only;
    it's not yet decided by the spline author (the moment) when to share the full process (merge and upload).
  - Finally create a milestone description and choose the previously created tag mentioning the
    changes that have been done.
  - For a bugfix adjust a given milestone to the new tag please; it's the same milestone and
    the description should not be repeated. Extend the description when reasonable.
