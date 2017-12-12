SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid bash code running in parallel" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-012.yaml 2>&1 | grep '\(second\|first\)'"
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| second - parallel one!" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| first - parallel one!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "| second - parallel two!" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "| first - parallel two!" ]
}