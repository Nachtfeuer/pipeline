SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid bash file" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-006.yaml
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "Processing pipeline stage 'test'" ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world!" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}