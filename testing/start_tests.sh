#!/bin/bash

cd code
mkdir /tmp/allure

pytest -s -l -v --alluredir=/tmp/allure