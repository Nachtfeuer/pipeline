SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid matrix filtered by first one" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-014.yaml --matrix-tags=first
    # verifying exit code
    [ ${status} -eq 0 ]

    # verifying output of second pipeline run
    [ "$(echo ${lines[-9]}|cut -d' ' -f6-)" == "Processing pipeline for matrix entry 'first'" ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| first hello world on matrix level" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}

@test "$BATS_TEST_FILENAME :: Testing valid matrix filtered by second one" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-014.yaml --matrix-tags=second
    # verifying exit code
    [ ${status} -eq 0 ]

    # verifying output of second pipeline run
    [ "$(echo ${lines[-9]}|cut -d' ' -f6-)" == "Processing pipeline for matrix entry 'second'" ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| second hello world on matrix level" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}