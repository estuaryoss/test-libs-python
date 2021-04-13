### Description

Excel export from json library used to support standardized testing.

![PyPI](https://img.shields.io/pypi/v/excel_generator)

## Programmatic example

```python
from excel_generator.generator import Generator

json_file = "results.json"
excel_file = "Results.xls"
generator = Generator(json_file=json_file, excel_file=excel_file)
generator.generate()
```

## Package call pypi

```shell
python -m excel_generator --infile results.json --outfile results.xls
```

### Set details

There are 3 ways to set the input variables for the CLI:

- Add an 'environment.properties' file containing: IN_FILE=results.json\nOUT_FILE=output.xls
- Set infile and outfile using an ENV VARs. E.g. export IN_FILE=results.json && export OUT_FILE=results.xls
- Set infile and outfile using CLI options '--infile' & '--outfile'

### Supported formats

## List of Dict(s) - Multiple messages (example)

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