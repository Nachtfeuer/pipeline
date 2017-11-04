#!/bin/bash
#             _ _     _       _
# __   ____ _| (_) __| | __ _| |_ ___
# \ \ / / _` | | |/ _` |/ _` | __/ _ \
#  \ V / (_| | | | (_| | (_| | ||  __/
#   \_/ \__,_|_|_|\__,_|\__,_|\__\___|
#
pykwalify \
    --verbose \
    --data-file ${PWD}/example.yaml \
    --schema-file ${PWD}/spline/schema.yaml
