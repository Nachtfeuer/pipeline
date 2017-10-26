SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-013.yaml
@test "$BATS_TEST_FILENAME :: Testing use of jinja" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-013.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "| 1:hello world!" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| 2:hello world!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| 3:hello world!" ]
}