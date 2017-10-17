SCRIPT="python ${WORKSPACE}/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-009.yaml
@test "$BATS_TEST_FILENAME :: Testing cleanup after pipeline run" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-009.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-6]}|cut -d' ' -f3-)" == "| cleanup has been called!" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f3-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| PIPELINE_RESULT=SUCCESS" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f3-)" == "| PIPELINE_SHELL_EXIT_CODE=0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
}