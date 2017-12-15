SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing cleanup after pipeline run" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-009.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| cleanup has been called!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| PIPELINE_RESULT=SUCCESS" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "| PIPELINE_SHELL_EXIT_CODE=0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
}