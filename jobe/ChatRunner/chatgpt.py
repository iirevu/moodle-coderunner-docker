# (C) 2025: Jonas Julius Harang, Hans Georg Schaathun <hasc@ntnu.no>

# This should be copied into the CodeRunner question.

from ChatRunner.chatrunner import *

# Inputs from Moodle
qid = {{ QUESTION.questionid }}

studans = """{{STUDENT_ANSWER | e('py') }}"""
studansraw = """{{ STUDENT_ANSWER | raw }}"""

graderstate_string = "{{ QUESTION.stepinfo.graderstate| json_encode | e('py')}}"

literatur = json.loads( "{{ literatur | json_encode(constant('JSON_UNESCAPED_UNICODE')) | e('py') | e('py')}}")

sandboxparams = json.loads("""{{ QUESTION.templateparams | json_encode | e('py') }}""")

# Load the problem text
with open('problem.md', 'r') as file:
    problem = file.read()

print( runAnswer( problem, studans, literatur, graderstate_string, sandboxparams, qid ) )
