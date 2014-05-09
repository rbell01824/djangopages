#!/bin/sh

./manage.py dumpdata --indent 4 | gzip > djangopages.json.gz
