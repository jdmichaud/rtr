#!/bin/sh
virtualenv python_modules
source python_modules/bin/activate
pip install -r requirements.txt
