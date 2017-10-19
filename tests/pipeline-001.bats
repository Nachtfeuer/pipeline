SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-001.yaml
@test "$BATS_TEST_FILENAME :: Testing valid inline bash code" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-001.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-8]}|cut -d' ' -f3-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Processing Bash code: finished" ]
}