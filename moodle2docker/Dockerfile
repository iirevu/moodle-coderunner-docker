FROM moodlehq/moodle-php-apache:8.3

RUN apt-get update && apt-get install -y cron

COPY crontab /

RUN crontab /crontab
