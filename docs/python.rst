The Python task
===============
Python behaves pretty the same way as a normal bash script
except that the code goes through the Python interpreter
found in the search path:

::

    model:
      message: 'hello world'

    pipeline:
        - stage(Example):
            - tasks(ordered):
                - python:
                    script: |
                        import sys
                        print(sys.version.replace("\n", ""))
                        print("{{ model.message }}{{ item }}!")
                    with:
                        - 1
                        - 2
                        - 3

Of course you can use Jinja2 templating accesing the model and the
environment variables or the item variable when using the  **width**
field. Also tags are allowed and you can specify a title for logging.
