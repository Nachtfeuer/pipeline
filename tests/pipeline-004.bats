SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-004.yaml
@test "$BATS_TEST_FILENAME :: Testing use of environment variables (stage level, merging)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-004.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-5]}|cut -d' ' -f3-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world at stage level!" ]
}