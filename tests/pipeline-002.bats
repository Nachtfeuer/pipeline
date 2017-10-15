SCRIPT="python ${WORKSPACE}/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-002.yaml
@test "$BATS_TEST_FILENAME :: Testing failing inline bash code" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-002.yaml
    # verifying exit code
    [ ${status} -eq 1 ]
    # verifying output
    [ "$(echo ${lines[-2]}|cut -d' ' -f3-)" == "Exit code has been 1" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f3-)" == "Pipeline has failed: immediately leaving!" ]
}