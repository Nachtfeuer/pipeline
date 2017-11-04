SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing use of environment variables (stage level, merging)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-004.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world at stage level!" ]
}