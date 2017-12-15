SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing use of environment variables (stage level, merging)" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-004.yaml 2>&1 | grep level"
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "| hello world at stage level!" ]
}