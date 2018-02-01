SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing cleanup when a shell has failed" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-010.yaml
    # verifying exit code
    [ ${status} -eq 1 ]
    # verifying output
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "| cleanup has been called!" ]
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| PIPELINE_RESULT=FAILURE" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| PIPELINE_SHELL_EXIT_CODE=123" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Pipeline has failed: leaving as soon as possible!" ]
}