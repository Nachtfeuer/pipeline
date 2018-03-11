Own Test Runner
===============

The test runner combines unittests and coverage:

::

    scripts/runner \
        --start-directory={toxinidir}/tests \
        --verbose \
        --randomly \
        --failfast \
        --cov-omit=.tox/*,tests/*,usr/* \
        --cov-fail-under=95

**Please note**: the runner is not yet production ready
because the coverage doesn't work when running through
tox. I havn't a clue yet why this is the case and will
udate the page when it is solved.

