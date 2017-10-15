#!/bin/bash
if [ ! -d bats-core ]; then
    git clone https://github.com/bats-core/bats-core.git
fi

# running all tests
WORKSPACE=$PWD bats-core/bin/bats tests
