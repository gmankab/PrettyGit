#!/bin/bash
rm -r dist
python -m hatchling build
# pip install --force-reinstall dist/*.whl --no-warn-script-location
cp dist/*.whl /mnt/ssd
