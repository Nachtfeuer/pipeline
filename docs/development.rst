Development
===========

Python Development
------------------
Many programming languages are providing essential language constructs
and tools which help to write code with acceptable quality and giving
you control to either keep or even to improve the quality constantly.
**A decrease in quality should always fail the build**.

For me it turned that **tox** is a very useful tool to organize the Python
build process (see **tox.ini**). Basically you define and reuse commands
for different Python (virtual) environments. It's a wrapper for **virtualenv**.
A good example is the definition for your tests:

::

    [tool-test]
    commands = 
        coverage erase
        coverage run    --omit={toxinidir}/.tox/*,{toxinidir}/tests/* --branch -m unittest discover -s {toxinidir}/tests -f -v
        coverage html   --title="Spline Code Coverage" --directory={toxinidir}/htmlcov
        coverage report --show-missing --fail-under={env:MIN_COVERAGE:95}

The calls:

::

    tox -e test     # running tests and coverage
    tox -e doctest  # running doctests only

The given example simply works with a standard Python installation and
one additional tool named **coverage** (`pip install coverage`). The unittesting
framework is capable of **discovering** all tests using following command:

::

    python -m unittest discover -s {toxinidir}/tests -f -v

The parameter `-s` specifies the folder to start with, the parameter `-v` (verbose) does show each
executed test method and the `-f` (failfast) stops immediately the tests on a failure.
Using `coverage run` instead of `python` the whole runs also with code coverage.
Additional parameters control what is included and/or excluded.
In given case the `.tox` folder should be excluded since it contains all Python libraries which shouldn't
be part of the coverage. In addition we would like to have more detailed information about the branch coverage.

The `coverage erase` ensure that results from a previous run do not influence
the new coverage calculation. Finally you should be interested in two reports:

 - **HTML report** - those one does show you the code in two colors: green=covered and red=not covered.
   It's easy then to see which tests you are missing.
 - **Console report** - those one gives you quick and short summary. As last report also 
   the limit is adjusted forcing the build to fail when the new coverage is less than the
   requested limit. A good orientation: try to have it greater or equal to 90%.

A special note on **MIN_COVERAGE**: Running the coverage for the spline project
with spline itself you cannot run the Docker based tests because usually you can't run
Docker inside Docker. Leaving out some tests the coverage will decrease and that's
why the required coverage is decreased via the pipeline.yaml (but still above 90%).

**How much coverage is needed?** Maybe the most frustrating fact is that even you
have 100% coverage the coverage is not necessarily complete. See following examples:

::

    def square(n):
        return n*n

Let's say you write tests like ``assert_that(square(2), equal_to(4))`` you might
think all is done but what happens if you call ``square('2')``?
You could argue that you wouldn't do that but as part of an calculation
where the input has been read from a file or from stdin the usecase might be
valid. Python doesn't enforce strict types.

::

    def square(n):
        return int(n) * int(n)

Now with this function you can handle both (However you still miss floats). I don't say you
should do that but the main focus here: also you have a coverage (line and branch) of 100% you
might miss valid usecases. What we can say for sure: if you have less than 100% 
coverage you certainly will miss usecases.

**Which test tool should be used?** Very well known are **nosetests** and **pytest**.
I leave it to you. For the spline project - trying to support many
different Python versions - it turned out to run better without them.

**What to do for static code analysis?** For a long time **pep8**, **pep257**, **pylint**,
**radon** and **flake8** are well known and often used tools. For pylint try to be as strict
as possible:

  - number of statements per method (or function)
  - number of lines per file
  - number of return statements
  - number of parameters

There are more but reducing those numbers you can force yourself
to care more on code design. Try to ensure that code complexity 
is as low as possible. Flake8 has an option to let it fail when
the complexity of your code exceeds a definable limit (for spline: 6).
Also try to keep line length acceptable; personally I wouldn't force
to 80 but 110 is a value I felt comfortable with. Keep in mind that
especially version diffs showing code side by side are influenced by this.

Some thrown warnings might annoy you sometimes but keeping the rules
also mean to keep your code style consistent and that cannot be done
without constant observation by tools. Before you commit your changes
to the code repository run all tests and all analysis to be on the safe
side. Here are the commands that can be used for individual checks:

::

    tox -e pep8
    tox -e pep257
    tox -e pylint
    tox -e flake8
    tox -e radon
    tox -e bandit

**What about documentation?** Tool documentation is one scenario
and everybody who is using the tool should have reasonable documentation.
You don't necessarily have to publish on read the docs but it should be easy
to find via the main page of the project. You can read the spline documentation
at read the docs as well as on the GitHub project. Another documentation is
API documentation and especially interesting for developers intending to use
the API. From what I have learned so far there are currently two good tools:

 - **Sphinx**: The tool is not necessarily bound to code; you can
   just write markdown text or reStructuredText like this article.
   In addition there are extensions that allow embedding diagrams
   and code. The documentation of the tool itself is quite good.
 - **epydoc**: this one is somehow similar to Doxygen and Javadoc; it seems
   that development has stopped (but that might have changed in the meantime).
   It's a very nice tool to get a good inside into the code.

I have used both. Please check the spline repository and also
see how they are defined in the **tox.ini**.

::

    tox -e sphinx  # generates read the doc HTML
    tox -e apidoc  # generates API HTML with Sphinx
    tox -e epydoc  # generates API HTML with epydoc


**What about packaging?** I decided to use wheel files. When
installing the wheel file in your system all dependencies are
installed as well. With **twine** (``pip install twine``) you
can easily upload the package to **PyPI**.

::

    tox -e package   # building the wheel file

I can advise only to be verbose in specifying the details
for your package in your **setup.py** because there is much
more than just uploading the code:

 - of course you have to specify **name** and **version**
 - the **long description** you should consider to read from a file
   and you can use reStructuredText.
 - specifying author and a mail address
 - specifying all package folders/paths
 - you can specify **scripts** to be installed (like **spline**)
 - you have to specify files that are not Python code (**package_data**)
 - define the runtime dependencies (**install_requires**)
 - The **url** can be any homepage for your component (tool or library)
 - The **classifiers** is a standardized way to tell more about
   your component like **status** and which Python versions are supported,
   which platforms are supported and other informations like that.

**How about testing Python versions you don't have on your machine?**
That has been one reason (there were others too) for writing the spline tool:

::

    spline --matrix-tags=py27   # runs tox -e py27 inside Docker
    spline --matrix-tags=py33   # runs tox -e py33 inside Docker
    spline --matrix-tags=py34   # runs tox -e py34 inside Docker
    spline --matrix-tags=py35   # runs tox -e py35 inside Docker
    spline --matrix-tags=py36   # runs tox -e py36 inside Docker
    spline --matrix-tags=pypy   # runs tox -e pypy inside Docker
    spline --matrix-tags=pypy3  # runs tox -e pypy3 inside Docker

Because the different Python processes are running inside a well
defined Docker container environment you are able to reproduce problems
without affecting your own machine.

**How about Travis CI?** If you have completed all mentioned tasks the
activating of Travis CI is easy. I have logged in with my GitHub account
choosing the public repository and that it's. Now you require a **.travis.yml**.
The file format is quite simple; there's good documentation at Travis CI
itself and you also can search for the file in the internet to find
sufficient examples. You also can check the variant I have used in the
spline project. The probably most interesting aspect for me was using of matrix
builds. Two packages require attention:

 - installation of `tox-travis` which ensures on a matrix build that tox understands
   which Python version has to be taken.
 - installation of `coveralls` allows you to send coverage reports to the
   central service https://coveralls.io/. It also integrates as build check
   when doing pull requests being able to block a merge when coverage has
   decreased.


Finally here are **some links** you might find useful:

 - https://tox.readthedocs.io/en/latest/
 - http://coverage.readthedocs.io/en/latest/
 - http://radon.readthedocs.io/en/latest/
 - https://pylint.readthedocs.io/en/latest/
 - https://pycodestyle.readthedocs.io/en/latest/
 - http://pep257.readthedocs.io/en/latest/
 - https://wiki.openstack.org/wiki/Security/Projects/Bandit
 - https://docs.python.org/2/library/unittest.html
 - https://docs.python.org/2/library/doctest.html
 - http://pyhamcrest.readthedocs.io/en/latest/
 - http://epydoc.sourceforge.net/
 - http://www.sphinx-doc.org/en/stable/rest.html
 - http://www.sphinx-doc.org/en/stable/ext/napoleon.html
 - https://docs.travis-ci.com/user/languages/python/
 - https://travis-ci.org/
 - https://coveralls.io/


That's it. Please let me know when you miss details here.
Also I'm interested in other tools that are useful for the
Python build process that help to keep/improve the quality.
Feel free to create a ticket (see issues on the GitHub page)
with the details. Of course I will always update this article
when I have new details.
