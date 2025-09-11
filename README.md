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
    + You will have to go through the setup procedure.
      In the database setup, you have to choose mariadb as
      the server type, and mariadb as the hostname.  The database
      user and password are found in the docker-compose.yml file.
    + Moodle will complain that you are not using SSL (https).  
      It still works, and for testing and prototyping there is no
      need to worry.  For production, this has to change.
5.  Configure Site Administration -> Plugins -> CodeRunner.
    Set Jobe server to «jobe».
5.  Configure Site Administration -> General -> HTTP Security.
    Prune the «cURL blocked hosts list».  It may suffice to remove
    the 172.* addresses, but this may depend on the configuration of
    docker.
6.  Run `docker exec -it /usr/local/bin/php  /var/www/html/admin/cli/cron.php`
    + Moodle usually requires a cron job, but cron works poorly in docker containers.  
    + You may have to rerun the above command regularly, but the critical issue is
      to run it once to have the question bank work.
    + In production it should be run from cron.


## Sample Question

To enter a sample question in CodeRunner, you can open a new question and make
the following changes.  This assumes that you have an API key with OpenAI.

1. Under CodeRunner Question type -> Question Type, select Python3
2. Enter the contents of file `jobe/ChatRunner/chatgpt.py` under Customisation -> Template
3. Under Customisation -> Grading, select Template grader

4. Enter the following under Advanced Customisation -> Sandbox -> Parameters:
```
{ "API": "openai", "model": "gpt-4o", "url": "https://api.openai.com/v1/chat/completions", "OPENAI_API_KEY": "<your key>" }
```
5. Under General, give the question a name and question text.  This does not matter
   for testing.  You can use sampel question text from `Example/problem.md` and
   «Mikroskopet» for question name.
6. Under support files, add the files from the Example directory:
   literature.json, problem.md, question.md
7. Testing the question, you may use `Example/naiveanswer.md` as a dummy answer.

Developing your own qestion, you change the files used in steps 5-7; everything else is
constant.

Using different language models, you change the sandbox parameters i Step 4.
