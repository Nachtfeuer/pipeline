SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing recursive Jinja2 template" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-019.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [[ "$output" =~ "test:env foo-The answer is 42." ]]
}
