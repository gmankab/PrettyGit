#!/bin/bash
rm ./dist/*
python -m hatchling build
pip install --no-warn-script-location --force-reinstall ./dist/prettygit-22.0.3-py3-none-any.whl
