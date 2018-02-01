SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing using a model" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-017.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "| Gandalf" ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| Carolinus" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| Belgarath" ]
}
