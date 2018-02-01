SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing use of environment variables (tasks level, merging)" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-005.yaml 2>&1 | grep level"

    # verifying output
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "| hello world at stage level!" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "| hello world at tasks level!" ]
}