SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing option --validate-only" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-001.yaml --validate-only
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output

    line=$(echo ${lines[-2]}|cut -d' ' -f6-)
    line=${line//$WORKSPACE/}
    [ "$line" == "Schema validation for '/tests/pipeline-001.yaml' succeeded" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Stopping after validation as requested!" ]
}

@test "$BATS_TEST_FILENAME :: Testing invalid pipeline definition" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-011.yaml --validate-only
    # verifying exit code
    [ ${status} -eq 1 ]
    # verifying output
    line=$(echo ${lines[-1]}|cut -d' ' -f6-)
    line=${line//$WORKSPACE/}
    [ "$line" == "Schema validation for '/tests/pipeline-011.yaml' has failed" ]
}