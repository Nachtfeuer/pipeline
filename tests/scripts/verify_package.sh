#!/bin/bash
VP_PROMPT=" verify_package.sh :: "

if [ $# -eq 0 ]; then
    echo "${VP_PROMPT}Running blank Docker container ..."
    docker run --rm -v $PWD:/mnt/host -i centos:7 /mnt/host/tests/scripts/verify_package.sh VERIFY
else
    # provide pip
    echo "${VP_PROMPT}Ensure pip tool is given ..."
    yum -y install python-setuptools
    easy_install pip

    # find wheel file in concrete version
    echo "${VP_PROMPT}Find wheel package in concrete version ..."
    package_version=$(grep VERSION /mnt/host/spline/version.py|cut -d'=' -f2|sed 's:[ "]*::g')
    wheel_file=$(find /mnt/host/dist -name "spline-${package_version}*.whl")

    # testing installation
    echo "${VP_PROMPT}Installing of ${wheel_file} ..."
    pip install ${wheel_file}
    verify_error=$?
    if [ ${verify_error} -eq 0 ]; then
        spline --definition=/mnt/host/tests/scripts/verify_package.yml
        verify_error=$?
    fi

    if [ ${verify_error} -eq 0 ]; then
        echo "${VP_PROMPT}Verifying wheel package succeeded!"
    else
        echo "${VP_PROMPT}Verifying wheel package Failed!"
    fi
    exit ${verify_error}
fi