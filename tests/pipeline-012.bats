SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-012.yaml
@test "$BATS_TEST_FILENAME :: Testing valid bash cod running in parallel" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-012.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-10]}|cut -d' ' -f6-)" == "Run tasks in parallel" ]
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "| second: parallel one!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| first: parallel one!" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Parallel Processing Bash code: finished" ]
}