SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing filtering by first tag" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-008.yaml --tags=one
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| hello world one!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}

@test "$BATS_TEST_FILENAME :: Testing filtering by second tag" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-008.yaml --tags=two
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| hello world two!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}

@test "$BATS_TEST_FILENAME :: Testing filtering by both tags" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-008.yaml --tags=one,two
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "| hello world one!" ]
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "Exit code has been 0" ]

    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| hello world two!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}
