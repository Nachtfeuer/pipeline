#!/bin/bash
bats_url=https://github.com/bats-core/bats-core.git

if [ ! -d bats-core ]; then
    echo "Downloading bats tool from ${bats_url}"
    git clone ${bats_url}
fi

WORKSPACE=$PWD
export WORKSPACE

# one simple run
python ${WORKSPACE}/pipeline --definition=tests/pipeline-001.yaml

# running all tests
bats-core/bin/bats tests
