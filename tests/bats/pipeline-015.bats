SCRIPT="python ${WORKSPACE}/scripts/spline"

@test "$BATS_TEST_FILENAME :: Testing valid Docker container (with no image specified)" {
    run bash -c "${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-015.yaml --tags=no-image 2>&1 | grep figlet"
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "| figlet: ....._............_............." ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| figlet: ..__|.|.___...___|.|._____._.__." ]
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| figlet: ./._\`.|/._.\./.__|.|/./._.\.'__|" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "| figlet: |.(_|.|.(_).|.(__|...<..__/.|..." ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "| figlet: .\__,_|\___/.\___|_|\_\___|_|..." ]
}

@test "$BATS_TEST_FILENAME :: Testing valid Docker container (with no remove)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-015.yaml --tags=no-remove
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| PIPELINE_STAGE=test" ]
    [ "$(echo ${lines[-3]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]

    [ "$(docker ps -a --format="{{.Names}}"|wc -l)" == "0" ]
}

@test "$BATS_TEST_FILENAME :: Testing valid Docker container (with mount)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/bats/pipeline-015.yaml --tags=using-mount
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world" ]
}
