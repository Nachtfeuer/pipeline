SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing use of environment variables (pipeline level)" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-003.yaml 2>&1 | grep 'pipeline level'"
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "| hello world at pipeline level!" ]
}