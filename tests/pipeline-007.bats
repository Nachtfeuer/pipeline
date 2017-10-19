SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-007.yaml
@test "$BATS_TEST_FILENAME :: Testing valid matrix with two entries" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-007.yaml
    # verifying exit code
    [ ${status} -eq 0 ]

    # verifying output of second pipeline run
    [ "$(echo ${lines[-18]}|cut -d' ' -f3-)" == "Processing pipeline for matrix entry 'first'" ]
    [ "$(echo ${lines[-17]}|cut -d' ' -f3-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-13]}|cut -d' ' -f3-)" == "| first hello world on matrix level" ]
    [ "$(echo ${lines[-11]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-10]}|cut -d' ' -f3-)" == "Processing Bash code: finished" ]

    # verifying output of second pipeline run
    [ "$(echo ${lines[-9]}|cut -d' ' -f3-)" == "Processing pipeline for matrix entry 'second'" ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f3-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| second hello world on matrix level" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Processing Bash code: finished" ]
}