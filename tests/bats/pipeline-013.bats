SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing use of jinja" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-013.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| 1:hello world!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| 2:hello world!" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| 3:hello world!" ]
}