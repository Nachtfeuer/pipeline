SCRIPT="python ${WORKSPACE}/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-005.yaml
@test "$BATS_TEST_FILENAME :: Testing use of environment variables (tasks level, merging)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-005.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-6]}|cut -d' ' -f3-)" == "| hello world at pipeline level!" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f3-)" == "| hello world at stage level!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world at tasks level!" ]
}