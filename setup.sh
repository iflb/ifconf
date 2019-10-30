#!/bin/bash

# reference
# https://packaging.python.org/tutorials/packaging-projects/
# https://qiita.com/shinichi-takii/items/e90dcf7550ef13b047b5

# before install
# ??? pip3 install readme-md
# pip3 install readme_renderer[md]
# python3 -m pip install --user --upgrade twine

rm -rf ifconf.egg-info/* dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

#python3 -m pip install --index-url https://test.pypi.org/ifconf/ --no-deps ifconf

#pip3 --no-cache-dir install --upgrade --index-url https://test.pypi.org/simple/ <パッケージ名>

# FOR real.
python3 -m twine upload --repository pypi dist/*

# then call
# pip3 install --index-url https://test.pypi.org/simple/ --no-deps ifconf for test, or
# pip3 install ifconf


