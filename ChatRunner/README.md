
+ chatgpt-orig.py is the original file, copied from the CodeRunner interface
+ chatgpt.py should replace it, but it depends on the following files
  being uploaded as supplementary files
    + chatrunner.py 
    + prompt.md
    + runnerstring.py

The question specific code is in prompt.md.

Probably, the python file chatrunner.py and runnerstring.py could both
be wrapped in a packaged and installed on the server with pip.  Being
generic, it should not be necessary to add them to each individual 
question.
