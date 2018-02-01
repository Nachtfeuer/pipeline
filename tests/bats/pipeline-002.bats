SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing failing inline bash code" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-002.yaml 2>&1 | grep -e '\(Exit\|leaving\)'"

    # verifying output
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 1" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Pipeline has failed: leaving as soon as possible!" ]
}