SCRIPT=${WORKSPACE}/pipeline

@test "$BATS_TEST_FILENAME :: Testing use of environment variables (pipeline level)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-003.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-4]}|cut -d' ' -f3-)" == "| hello world at pipeline level!" ]
}