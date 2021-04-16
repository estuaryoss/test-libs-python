### Description

Fluentd logging library used to support standardized testing. Takes as input an Excel document.  
The Excel document can be generated with [excel_generator](https://github.com/estuaryoss/test-libs-python/tree/master/excel_generator)

![PyPI](https://img.shields.io/pypi/v/zephyr-uploader)

### Description

Upload test results in Jira Zephyr library used to support standardized testing.

### Call example

```bash
python -m zephyr_uploader --username auto-robot --password mySecretPasswd123! \
--jira_url http://jira.yourcompany.com/rest/ --project_key AIP --release_version 1.2-UP2020 --test_cycle Regression --report_path Regression_FTP.xls \
--no_of_threads=10 --folder_name Results --recreate_folder false 
```

## Programmatic example from Excel file

```python
zephyr_config_dict = {
        CliConstants.USERNAME: username,
        CliConstants.PASSWORD: password,
        CliConstants.JIRA_URL: jira_url,
        CliConstants.TEST_CYCLE: test_cycle,
        CliConstants.PROJECT_KEY: project_key,
        CliConstants.RELEASE_VERSION: release_version,
        CliConstants.REPORT_PATH: report_path,
        CliConstants.FOLDER_NAME: folder_name,
        CliConstants.NO_OF_THREADS: no_of_threads,
        CliConstants.RECREATE_FOLDER: recreate_folder,
        CliConstants.COMMENTS_COLUMN: comments_column,
        CliConstants.EXECUTION_STATUS_COLUMN: execution_status_column
    }
# zephyr_config_dict = EnvLoader().get_zephyr_config_from_env() <-use this one if you use an 'environment.properties'
zephyr_configurer = ZephyrConfigurer(zephyr_config_dict)
zephyr_configurer.validate()

try:
    sheet = pyexcel.get_sheet(file_name=zephyr_configurer.get_config().get(CliConstants.REPORT_PATH.value))
    excel_data = sheet.to_array()
    zephyr_uploader = ZephyrUploader(ZephyrService(zephyr_configurer))
    zephyr_uploader.upload_jira_zephyr(excel_data=excel_data)
except Exception as e:
    print(e.__str__())
```

## Programmatic example with more granularity

```python
folder_name_with_timestamp = self.config.get(CliConstants.FOLDER_NAME.value) + "_" + date.today().strftime(
            "%Y-%m-%d")

project_id = self.zephyr_service.get_project_id_by_key(self.config.get(CliConstants.PROJECT_KEY.value))
version_id = self.zephyr_service.get_version_for_project_id(self.config.get(CliConstants.RELEASE_VERSION.value),
                                                            project_id=project_id)
cycle_id = self.zephyr_service.get_cycle_id(self.config.get(CliConstants.TEST_CYCLE.value), project_id,
                                            version_id)
folder_id = self.zephyr_service.get_folder_id(folder_name=folder_name_with_timestamp, cycle_id=cycle_id,
                                              project_id=project_id, version_id=version_id)

if folder_id is not None and self.config.get(CliConstants.RECREATE_FOLDER.value):
    self.zephyr_service.delete_folder_from_cycle(folder_id=folder_id, project_id=project_id,
                                                 version_id=version_id, cycle_id=cycle_id)
    time.sleep(5)
    folder_id = self.zephyr_service.create_folder_under_cycle(folder_name=folder_name_with_timestamp)

if folder_id is None:
    folder_id = self.zephyr_service.create_folder_under_cycle(folder_name=folder_name_with_timestamp)

sheet = pyexcel.get_sheet(file_name=zephyr_configurer.get_config().get(CliConstants.REPORT_PATH.value))
excel_data = sheet.to_array()

for row in excel_data:
  jira_id = row[0]
  issue_id = self.zephyr_service.get_issue_by_key(jira_id)
  execution_id = self.zephyr_service.create_new_execution(issue_id=issue_id, zephyr_meta_info=zephyr_meta_info)
  if row[self.config.get(CliConstants.EXECUTION_STATUS_COLUMN.value)] == ExecutionStatus.SUCCESS.value:
      self.zephyr_service.update_execution(execution_id, TestStatus.PASSED.value,
                                           row[self.config.get(CliConstants.COMMENTS_COLUMN.value)])
  elif row[self.config.get(CliConstants.EXECUTION_STATUS_COLUMN.value)] == ExecutionStatus.FAILURE.value:
      self.zephyr_service.update_execution(execution_id, TestStatus.FAILED.value,
                                           row[self.config.get(CliConstants.COMMENTS_COLUMN.value)])
  else:
      self.zephyr_service.update_execution(execution_id, TestStatus.NOT_EXECUTED.value,
                                           row[self.config.get(CliConstants.COMMENTS_COLUMN.value)])
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