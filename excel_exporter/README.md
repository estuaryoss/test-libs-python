### Description
Excel export from json library used to support standardized testing.

### Call example
```bash
python main.py --infile results.json --outfile results.xls
```

### Set details
There are 3 ways to set the location of fluentd IP:PORT:
-   Add an 'environment.properties' file containing: IN_FILE=results.json\nOUT_FILE=output.xls
-   Set infile and outfile using an ENV VARs. E.g. export IN_FILE=results.json && export OUT_FILE=results.xls 
-   Set infile and outfile using CLI options '--infile' & '--outfile'

### Supported formats

## List of Dict(s) - multiple test result (example)
```json
[
{"testName": "exampleTest1", "Db": "Mysql57", "OS":"Centos7", "logLocation": "http://logdatabase.com/exampleTest1", 
"startedat":  "Sun Nov  1 10:16:52 EET 2020", "endedat":  "Sun Nov  1 10:22:52 EET 2020", ...otherinformation},
{"testName": "exampleTest2", "Db": "Mysql57", "OS":"Centos7", "logLocation": "http://logdatabase.com/exampleTest2", 
"startedat":  "Sun Nov  1 10:22:52 EET 2020", "endedat":  "Sun Nov  1 10:30:52 EET 2020", ...otherinformation}
... other tests

]
```
