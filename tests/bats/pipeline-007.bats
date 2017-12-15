SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid matrix with two entries" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-007.yaml
    # verifying exit code
    [ ${status} -eq 0 ]

    # verifying output of second pipeline run
    [ "$(echo ${lines[-16]}|cut -d' ' -f6-)" == "Processing pipeline for matrix entry 'first'" ]
    [ "$(echo ${lines[-15]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-11]}|cut -d' ' -f6-)" == "| first hello world on matrix level" ]
    [ "$(echo ${lines[-10]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-9]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]

    # verifying output of second pipeline run
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "Processing pipeline for matrix entry 'second'" ]
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| second hello world on matrix level" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}