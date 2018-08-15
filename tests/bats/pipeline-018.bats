SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing Tasks With using a model" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-018.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [[ "$output" =~ "---1---" ]]
    [[ "$output" =~ "---2---" ]]
    [[ "$output" =~ "---3---" ]]

    result=$(echo "$output" | grep -- '---' | wc -l)
    [ $result -eq 3 ]
}
