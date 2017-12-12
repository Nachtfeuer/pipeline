SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing use of environment variables (tasks level, merging)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-005.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| hello world at stage level!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world at tasks level!" ]
}