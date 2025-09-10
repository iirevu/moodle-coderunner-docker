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

## Usage

1.  Make sure you have git, docker, and docker-compose.
2.  Run `sh gitclone.sh` to set up the moodle directory.
3.  Run `docker compose up -d` to start the server.
4.  Connect to http://localhost:8080/

You will have to go through the setup procedure.
In the database setup, you have to choose mariadb as
the server type, and mariadb as the hostname.  The database
user and password are found in the docker-compose.yml file.

Moodle will complain that you are not using SSL (https).  
It still works, and for testing and prototyping there is no
need to worry.  For production, this has to change.

