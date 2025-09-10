# SECRET key required

K="<secret key here>"

U="https://api.openai.com/v1/chat/completions"
# M=deepseek-r1
M=gpt-4o


L=Example/literature.json 
P=Example/problem.md 
A=Example/naiveanswer.md

python3 -m ChatRunner -l $L -k "$K" -u $U -m $M -A openai  $* $P $A

