SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-008.yaml

@test "$BATS_TEST_FILENAME :: Testing filtering by first tag" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-008.yaml --tags=one
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-8]}|cut -d' ' -f3-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world one!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Processing Bash code: finished" ]
}

@test "$BATS_TEST_FILENAME :: Testing filtering by second tag" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-008.yaml --tags=two
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-8]}|cut -d' ' -f3-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world two!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Processing Bash code: finished" ]
}

@test "$BATS_TEST_FILENAME :: Testing filtering by both tags" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-008.yaml --tags=one,two
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-10]}|cut -d' ' -f3-)" == "| hello world one!" ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f3-)" == "Exit code has been 0" ]

    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world two!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Processing Bash code: finished" ]
}
