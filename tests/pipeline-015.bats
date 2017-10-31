SCRIPT="python ${WORKSPACE}/scripts/pipeline"

# From the root of the repository you also can test this
# with following command. ./pipeline --definition=tests/pipeline-015.yaml

@test "$BATS_TEST_FILENAME :: Testing valid Docker container (with no image specified)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-015.yaml --tags=no-image
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-9]}|cut -d' ' -f6-)" == "| ....._............_............." ]
    [ "$(echo ${lines[-8]}|cut -d' ' -f6-)" == "| ..__|.|.___...___|.|._____._.__." ]
    [ "$(echo ${lines[-7]}|cut -d' ' -f6-)" == "| ./._\`.|/._.\./.__|.|/./._.\.'__|" ]
    [ "$(echo ${lines[-6]}|cut -d' ' -f6-)" == "| |.(_|.|.(_).|.(__|...<..__/.|..." ]
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| .\__,_|\___/.\___|_|\_\___|_|..." ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]
}

@test "$BATS_TEST_FILENAME :: Testing valid Docker container (with no remove)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-015.yaml --tags=no-remove
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-5]}|cut -d' ' -f6-)" == "| PIPELINE_STAGE=test" ]
    [ "$(echo ${lines[-2]}|cut -d' ' -f6-)" == "Exit code has been 0" ]
    [ "$(echo ${lines[-1]}|cut -d' ' -f6-)" == "Processing Bash code: finished" ]

    [ "$(docker ps -a --format="{{.Names}}"|wc -l)" == "0" ]
}

@test "$BATS_TEST_FILENAME :: Testing valid Docker container (with mount)" {
    run ${SCRIPT} --definition=${WORKSPACE}/tests/pipeline-015.yaml --tags=using-mount
    # verifying exit code
    [ ${status} -eq 0 ]
    # verifying output
    [ "$(echo ${lines[-4]}|cut -d' ' -f6-)" == "| hello world" ]
}
