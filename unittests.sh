#!/bin/bash
if [ ! -d bats-core ]; then
    git clone https://github.com/bats-core/bats-core.git
fi

WORKSPACE=$PWD
export WORKSPACE

# one simple run
python ${WORKSPACE}/pipeline --definition=tests/pipeline-001.yaml

# running all tests
bats-core/bin/bats tests
