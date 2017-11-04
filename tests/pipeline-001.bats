SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid inline bash code" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-001.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-15]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-12]}|cut -d' ' -f6-)" == "print out hello world" ]
    [ "$(echo ${lines[-10]}|cut -d' ' -f6-)" == "| hello world 1!" ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]

    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world 2!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}