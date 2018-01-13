#!/bin/bash
rm -rf dist
rm -rf build
rm -f MANIFEST
rm -f pylint.log
rm -f pep8.log
rm -f pep257.log
rm -f flake8.log
rm -f .coverage
rm -f coverage.xml
rm -rf coverage
rm -f tests.xml
rm -f $(find . -name "*.pyc")
rm -f ccm.xml
rm -rf venv
rm -rf .tox
rm -rf .eggs
rm -rf pipeline.egg-info
rm -f .coverage.*
