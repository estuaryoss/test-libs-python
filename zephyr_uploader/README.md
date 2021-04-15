### Description

Fluentd logging library used to support standardized testing. Takes as input an Excel document.  
The Excel document can be generated with [excel_generator](https://github.com/estuaryoss/test-libs-python/tree/master/excel_generator)

![PyPI](https://img.shields.io/pypi/v/zephyr_uploader)

### Description

Upload test results in Jira Zephyr library used to support standardized testing.

### Call example

```bash
python -m zephyr_uploader --username auto-robot --password mySecretPasswd123! \
--jiraUrl http://jira.yourcompany.com/rest/ --projectKey AIP --releaseVersion 1.2-UP2020 --testCycle Regression --reportPath Regression_FTP.xls \
--noOfThreads=10 --folderName Results --recreateFolder false 
```

## Programmatic example

```python
# TODO
```

## ! Keep in mind

- You must have a column with the status of each test execution, and the values permitted are: SUCCESS / FAILURE. If
  none is present the test execution will be mapped as 'not executed'.
- You must specify the position of the above column from the Excel file. Default is the 6'th column. If you have the
  execution status on a different column please specify the position with the parameter 'executionStatusColumn'.   
  E.g. -executionStatusColumn=6
- You also can specify the comments column. For example the link where the test logs are. The default is 8'th column.   
  E.g. -commentsColumn=8
- Jira Ids column is always the first column in the Excel sheet

## Precedence

The arguments set with CLI are stronger than the ones from environment (env vars or 'environment.properties'
file).