#!/bin/sh

./manage.py dumpdata --natural --indent 4 | gzip > djangopages.json.gz
