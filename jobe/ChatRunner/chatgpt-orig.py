import subprocess, ast,re, base64, json

class Test:
   def __init__(self, testName=None):
      self.result = {"name": testName, "passed": False}

   def addResult(self, field_name, field_data):
      """
      Add resultdata. Data has a key (field_name) and value (field_data)
      """
      self.result.update({field_name: field_data})

   def addResults(self, res_dict):
      for k, v in res_dict.items():
         self.addResult(k,v)

   def pass_test(self, passed):
      self.result["passed"] = passed

   def __str__(self):
      return json.dumps(self.result, indent=4)

   def __repr__(self):
      return json.dumps({"Testobject": self.result})

   def load(self, str_repr):
      try:
         obj = json.loads(str_repr)
         self.result = obj["Testobject"]
         return True
      except:
         return False

   def dump(self):
      return self.__repr__()


class TestResults:
   """
   exitCode: 0:OK, 1:Feil/kræsj, 2:timeout, -1: Ingen tester å kjøre, -2:Testnummer finnes ikke
   output: Output fra testprogram
   """
   def __init__(self, output, exitCode=0, name=None):
      self.testresults = []
      self.other_output = ""
      self.exitCode = exitCode
      self.frac = 0
      self.name = name
      self.tableHeader = None
      self.tableRemap = None
      self.resultstable = None
      if exitCode != 0:
         self.results = {"failed": {"description": "CodeTester ran without loaded tests"}}
         return

      test = Test()
      for line in output.splitlines():
         if test.load(line):
            self.testresults.append(test)
            test = Test()
         else:
            self.other_output+= line+"\n"
      self.numTests = len(self.testresults)

   def makeResultTable(self, tableHeader, tableRemap):
      self.tableHeader = tableHeader
      self.resultstable = [tableHeader]

      if not tableRemap:
         tableRemap = {k:k for k in tableHeader}
      else:
         for header in tableHeader:
            if header not in tableRemap.keys():
               tableRemap.update({header:header})

      self.tableRemap = tableRemap
      for test in self.testresults:
         row = []
         for column in self.tableHeader:
            try:
               row.append(test.result[tableRemap[column]])
            except:
               row = []
               break
         if row != []:
            self.resultstable.append(row)

   def __repr__(self):
      data = {"TestResultsObj": {
            "testresults": [t.dump() for t in self.testresults],
            "other_output": self.other_output,
            "tableHeader": self.tableHeader,
            "tableRemap": self.tableRemap,
            "resultstable": self.resultstable,
            "frac": self.frac,
            "name": self.name
         }
      }
      return json.dumps(data)

   def dump(self):
      return self.__repr__()

   def load(self, str_repr):
      obj_read = False
      self.unencoded = ""
      for line in str_repr:
         try:
            data = json.loads(line)
            obj = data["TestResultsObj"]
            self.testresults = [Test() for res in obj["testresults"]]
            self.testresults = list(map(Test.load, self.testresults))
            self.other_output = obj["other_output"]
            self.tableHeader = obj["tableHeader"]
            self.tableRemap = obj["tableRemap"]
            self.resultstable = obj["resultstable"]
            self.frac = obj["frac"]
            self.name = obj["name"]
            obj_read = True
         except:
            self.unencoded += line + '\n'
      return obj_read

   def mark(self):
      total_marks = 0
      obtained_marks = 0
      for test in self.testresults:
         if "mark" in test.result.keys():
            mark = test.result["mark"]
            total_marks += mark
         else:
            mark = 0
         if test.result["passed"]:
            obtained_marks += mark
      if total_marks != 0:
         self.frac = obtained_marks/total_marks
      else:
         self.frac = 0

   def getCodeRunnerOutput(self, prehtml=None, posthtml=None, graderstate=None, other_lines=False):
      json_str = json.dumps({"fraction": self.frac,
                      "testresults": self.resultstable,
                      "prologuehtml": prehtml,
                      "epiloguehtml": posthtml,
                      "graderstate": graderstate}, ensure_ascii=False)

      if other_lines:
         prehtml = f"""<h2> Other output / error-messages from testgrader </h2>
         <p><br>
         """+self.other_output.replace("\n", "<br>")+"""
         </p></br>"""
      return json.dumps({"fraction": self.frac,
                      "testresults": self.resultstable,
                      "prologuehtml": prehtml,
                      "epiloguehtml": posthtml,
                      "graderstate": graderstate}, ensure_ascii=False)
   def mergeResults(self, merging_result):
      if self.resultstable == None:
         if merging_result.resultstable == None:
            pass
         else:
            self.resultstable=merging_result.resultstable
            self.tableHeader = merging_result.tableHeader
            self.tableRemap = merging_result.tableRemap
      elif merging_result.resultstable == None:
         pass
      else:
         self.resultstable = self.resultstable + merging_result.resultstable[1:]

      self.other_output += merging_result.other_output
      self.testresults = self.testresults+merging_result.testresults


class CodeGrader:
   def __init__(self,test_programs):
      if type(test_programs) == list:
         self.test_programs = test_programs
      else:
         self.test_programs = [test_programs]

   def runTest(self, num=0, timeout=1.0):

      if not self.test_programs:
         return TestResults(None, -1)

      if num >= len(self.test_programs):
         return TestResults(None,-2)

      try:
         with open("code.py", "w") as fout:
             fout.write(self.test_programs[num])
         sp = subprocess.run(['python3', 'code.py'],
             stderr=subprocess.STDOUT, universal_newlines=False, timeout=timeout, stdout=subprocess.PIPE)
         output = sp.stdout.decode()
         return TestResults(output)
      except subprocess.CalledProcessError as e:
         output = e.stdout.decode()
         return TestResults(output, exitCode=1)
      except subprocess.TimeoutExpired as e:
         output = e.stdout
         if output:
            output= output.decode()
         else:
             output = "Ingen output fra testprogrammet"
         return TestResults(output, exitCode=2)



def make_data_uri_image(filename):
    with open(filename, 'br') as fin:
        contents = fin.read()
    contents_b64 = base64.b64encode(contents).decode('utf8')
    if filename.endswith('.png'):
        return "data:image/png;base64,{}".format(contents_b64)
    elif filename.endswith('.jpeg') or filename.endswith('.jpg'):
        return "data:image/jpeg;base64,{}".format(contents_b64)
    else:
        return Exception("Unknown file type passed to make_data_uri_image (supported are .png and .jpg/jpeg")

def decorateStudFunction(decorator_name, functionname, codestring):
   decorated_code = re.sub(rf"(^\s*def {functionname}.*:)",rf"@{decorator_name}\1",codestring, flags = re.MULTILINE)
   return decorated_code

import json, re, sys
import numpy as np
 


qid = {{ QUESTION.questionid }}

studans = """
{{STUDENT_ANSWER | e('py') }}
"""
test_program = """
import subprocess, ast,re, base64, json

class Test:
   ...
class TestResults:
   ...
class CodeGrader:
   ...

import json, re
import numpy as np

import requests   # !!!


__student_answer__ =\"\"\"
{{ STUDENT_ANSWER | raw }}\"\"\"

literatur = json.loads(\"{{ literatur | json_encode(constant('JSON_UNESCAPED_UNICODE')) | e('py') | e('py')}}\")

openai_url = \"https://api.openai.com/v1/chat/completions\"

sandboxparams = json.loads({{ QUESTION.sandboxparams | json_encode | e('py') }})

graderstate_string = \"{{QUESTION.stepinfo.graderstate | json_encode | e('py') | e('py') }}\"
if not graderstate_string in [\"\", \"''\", \"null\", \"[]\"]:
   gs = json.loads(graderstate_string)
else:
   gs = None
try:
   prevans = gs[\"studans\"][-1]
except:
   prevans = \"Ingen tidligere svar gitt\"

chat_rolle = \"\"\"Du er læringsassistent som skal veilede studenter som har fått følgende oppgave
```html
<h3> Mikroskopet </h3>
<p>
Forklar oppbyggingen og virkemåten til et optisk mikroskop. <br>
Grei ut om de ulike delene og forklar kort hva de gjør.
</p>
<p>
Du skal gå litt mer i detalj på det optiske oppsettet:
<ul>
     <li> Hvordan skjer forstørringen i et mikroskop? </li>
     <li> Hvorfor bruker vi flere linser? </li>
</ul>
Til eksamen ville det her være viktig å tegne en skisse av hvordan forstørring foregår, her kan du heller oppgi en link til et bilde du synes forklarer linseoppsettet godt.
</p>
```

Du skal gi svaret som en gyldig JSON-streng på følgende måte:
[{\"testName\": navn, \"description\": beskrivelse, 
\"iscorrect\": true/false,  \"resultat\": resultat}, ]

Verdiene i listen er tester/eller momenter man burde ha med i besvarelsen.
Hver test har et navn, \"testName\" eller en beskrivelse som er kort nok til å vises i tabellformat.

\"description\" er en beskrivelse av testen som er kort nok til å passe inn i en tabell.

\"iscorrect\"  er en bool som angir om studenten passerer testen. 

\"Resultat\" er den formative tilbakemeldingen. Her går vi inn i hvordan svaret til studenten er bra eller mangelfult, og prøver så langt det
lar seg gjøre å gi gode hint om forbedringspotensiale, uten å direkte gi fasitsvaret.
\"Resultat\" teksten har html-format og Mathjax-notasjon kan også brukes. 
Dersom du trenger å vise til et linseoppsett for studenten, kan vise: \"https://jonajh.folk.ntnu.no/img/instrumentering/mikroskop-linser.png\"

Målet er formativ vurdering som hjelper studenten på vei.
Svar kun med listen av tester -- den evalueres i python med json.loads( ), selv i tilfeller med feks, tomt svar fra student

Under følger et sammensetning/sammendrag fra relevante deler av studentenes pensumliteratur. Du kan refere til sidetall her om det behøves
\"\"\"
chat_rolle += json.dumps(literatur, ensure_ascii = False)
chat_rolle += \"\"\"
All tekst som potensielt vises til studenten skal være på norsk. 
Studentens forrige svar (dersom det finnes): \"\"\"
chat_rolle += prevans



headers = { \"Authorization\": f\"Bearer {sandboxparams['OPENAI_API_KEY']}\",
            \"Content-Type\": \"application/json\"
          }
data = {\"model\": \"gpt-4o\",
        \"messages\": [{\"role\": \"system\", 
                          \"content\": chat_rolle
                     },
                     {\"role\": \"user\", \"content\": __student_answer__}]
       }




response = requests.post(openai_url, headers=headers, json=data)
svar = response.json()[\"choices\"][0][\"message\"][\"content\"]
svar_fetched = re.search(r\"\\[.*\\]\", svar, flags=re.DOTALL).group(0)

testResults =[]

for test in json.loads(svar_fetched):
   test_obj = Test(testName=test[\"testName\"])
   test_obj.addResult(\"mark\", 1)
   for k,v in test.items():
      if k == 'iscorrect':
         test_obj.pass_test(v)
      elif k == \"testName\":
         continue
      else:
         test_obj.addResult(k,v)
   testResults.append(test_obj)

svardata = Test(testName=\"svardata\")
svardata.addResult(\"gpt_svar\", json.dumps(svar))
print(svardata.dump())

for test in testResults:
   print(test.dump())

"""

graderstate_string = "{{ QUESTION.stepinfo.graderstate| json_encode | e('py')}}"

step = 0
if (not graderstate_string in ['null', '""', "''", '', '[]']):
   graderstate = json.loads(graderstate_string)
   step = graderstate["step"]
   graderstate["studans"].append(studans)
else:
   graderstate = {"step": 0, "studans": [studans], "svar": []}


test = CodeGrader([test_program])
testResults=test.runTest(num=0, timeout=40.0)

tableRemap = {"iscorrect": "passed", "Test": "name", "Beskrivelse": "description"}
tableHeader = ["iscorrect", "Test", "Beskrivelse"]

testResults.makeResultTable(tableHeader,tableRemap)
testResults.mark()

for test in testResults.testresults:
   if test.result["name"] == "svardata":
      graderstate["svar"].append(test.result["gpt_svar"])

graderstate["step"] += 1

phtml = ""

for test in testResults.testresults:
   result = test.result
   feedback = False
   if result["passed"]:
      color = "Lime"
      feedback = True
   elif "resultat" in result.keys():
      feedback = True
      color = "Red"
   if feedback:
      phtml += f"""
<h2 style="background-color:{color};">{result["name"]}</h2>
<p>{result["resultat"]} </p>
"""

print(testResults.getCodeRunnerOutput(other_lines=True, posthtml=phtml, graderstate=graderstate))
