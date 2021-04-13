### Description

Fluentd logging library used to support standardized testing.

## Programmatic example (Object logging)

```python
from fluent import sender
from fluentd_logger.logger import Logger

tag = "agent"
app_label = "api"

logger = sender.FluentSender(tag=tag, host="localhost", port=24224)
service = Logger(logger)

messages = [
  {
    "A": "A1",
    "B": "B1"
  },
  {
    "C": "C1",
    "D": "D1"
  }
]

for message in messages:
  service.emit(app_label=app_label, msg=message)
```

## Package call pypi (File logging)

```shell
python -m fluentd_logger --file results.json --tag agent --label api --fluentd localhost:24224
```

### Set --fluentd, --tag, --label options

There are 3 ways to set the above options

- Add an 'environment.properties' file containing the values. E.g.
  ```properties
  FLUENTD_IP_PORT=localhost:24224
  TAG=Agent
  LABEL=api
  ```
- Set the options through env vars. E.g.
  ```shell
  export FLUENTD_IP_PORT=localhost:24224, 
  export TAG=Agent
  export LABEL=4.2.1
  ```
- Set the values using this CLI interactively

### Supported formats

## Dict - one single test result (example)

```json
{
  "testName": "exampleTest",
  "Db": "Mysql57",
  "OS": "Centos7",
  "logLocation": "http://logdatabase.com/exampleTest",
  "startedat": "Sun Nov  1 10:16:52 EET 2020",
  "endedat": "Sun Nov  1 10:22:52 EET 2020"
}
```

## List of Dict(s) - multiple test result (example)

```json
[
  {
    "testName": "exampleTest1",
    "Db": "Mysql57",
    "OS": "Centos7",
    "logLocation": "http://logdatabase.com/exampleTest1",
    "startedat": "Sun Nov  1 10:16:52 EET 2020",
    "endedat": "Sun Nov  1 10:22:52 EET 2020"
  },
  {
    "testName": "exampleTest2",
    "Db": "Mysql57",
    "OS": "Centos7",
    "logLocation": "http://logdatabase.com/exampleTest2",
    "startedat": "Sun Nov  1 10:22:52 EET 2020",
    "endedat": "Sun Nov  1 10:30:52 EET 2020"
  }
]
```
