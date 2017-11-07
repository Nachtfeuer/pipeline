SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing parallel matrix with three entries" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-016.yaml 2>&1 | grep done"
    # verifying exit code
    [ ${status} -eq 0 ]

    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "| done - sleep 2s" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "| done - sleep 4s" ]
}