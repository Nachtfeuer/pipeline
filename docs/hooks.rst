Hooks
=====
Hooks are defined at same root level as the pipeline or the matrix.

The cleanup hook
----------------
It's basically same as for a shell script with a few differences only:

 - When the pipeline succeeds all variables from pipeline level are available.
 - When a shell script fails all variables on that level are available
 - Additionally the variable **PIPELINE_RESULT** can have the value **SUCCESS** or **FAILURE**.
 - Additionally the variable **PIPELINE_SHELL_EXIT_CODE** has the shell exit code
   of the failed shell or 0 (default)

::

    hooks:
        cleanup:
            script: |
                echo "cleanup has been called!"
                echo "${message}"
                echo "PIPELINE_RESULT=${PIPELINE_RESULT}"
                echo "PIPELINE_SHELL_EXIT_CODE=${PIPELINE_SHELL_EXIT_CODE}"
