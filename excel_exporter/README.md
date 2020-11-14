### Description
Fluentd logging library used to support standardized testing.

### Call example
```bash
python main.py --tag tag --file README.md --fluentd 129.168.0.100:24224
```

### Set Fluentd IP:PORT location
There are 3 ways to set the location of fluentd IP:PORT:
-   Add an 'environment.properties' file containing the location of the fluentd service. E.g. FLUENTD_IP_PORT=localhost:24224  
-   Set fluentd IP:PORT using an env VAR. E.g. export FLUENTD_IP_PORT=localhost:24224  
-   Set fluentd IP:PORT using the option '-fluentd' from the Main class of the jar for jar invocation  

### Supported formats

## Dict - one single test result (example)
```json
{"testName": "exampleTest", "Db": "Mysql57", "OS":"Centos7", "logLocation": "http://logdatabase.com/exampleTest", 
"startedat":  "Sun Nov  1 10:16:52 EET 2020", "endedat":  "Sun Nov  1 10:22:52 EET 2020", ...otherinformation}
```

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
