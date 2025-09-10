# CodeRunner Docker Environment

This setup is inspired by the 
[bitnami repository](https://github.com/bitnami/bitnami-docker-moodle for configuration parameters),
but the docker images have been replaced with an official database
image and a web server image from Moodle.

The purpose of this repo is to test a setup using large language
models (LLM) to provide automated feedback.  For this purpose CodeRunner
is used.  Even though CodeRunner is made for programming tasks,
it is here used only for free form text.  The programming 
features are used to pass student responses to the LLM.

Under `jobe/ChatRunner` there is a python package to provide the
API to call an LLM from CodeRunner.
