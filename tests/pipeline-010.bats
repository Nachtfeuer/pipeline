SCRIPT="python ${WORKSPACE}/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-010.yaml
@test "$BATS_TEST_FILENAME :: Testing cleanup when a shell has failed" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-010.yaml
    # verifying exit code
    [ ${status} -eq 123 ]
    # verifying output
    [ "$(echo ${lines[-7]}|cut -d' ' -f3-)" == "| cleanup has been called!" ]
    [ "$(echo ${lines[-6]}|cut -d' ' -f3-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f3-)" == "| PIPELINE_RESULT=FAILURE" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| PIPELINE_SHELL_EXIT_CODE=123" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Pipeline has failed: immediately leaving!" ]
}