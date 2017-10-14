#!/bin/bash
pykwalify -v \
    --data-file ${PWD}/example.yaml \
    --schema-file ${PWD}/schema.yaml
