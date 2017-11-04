SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid bash code running in parallel" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-012.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-22]}|cut -d' ' -f6-)" == "Run tasks in parallel" ]
    [ "$(echo ${lines[-17]}|cut -d' ' -f6-)" == "| second - parallel one!" ]
    [ "$(echo ${lines[-14]}|cut -d' ' -f6-)" == "| first - parallel one!" ]
    [ "$(echo ${lines[-11]}|cut -d' ' -f6-)" == "Parallel Processing Bash code: finished" ]

    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "| second - parallel two!" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| first - parallel two!" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Parallel Processing Bash code: finished" ]
}