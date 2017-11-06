#!/bin/bash
bats_url=https://github.com/bats-core/bats-core.git

if [ ! -d bats-core ]; then
    echo "Downloading bats tool from ${bats_url}"
    git clone ${bats_url}
fi

WORKSPACE=$PWD
export WORKSPACE
PYTHONPATH=$PWD
export PYTHONPATH

# one simple run
python ${WORKSPACE}/scripts/spline --definition=tests/pipeline-016.yaml

# running all tests
bats-core/bin/bats tests
