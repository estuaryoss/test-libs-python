#!/usr/bin/env python3
from datetime import date

import click

__author__ = "Catalin Dinuta"

import pyexcel

from zephyr_uploader.zephyr_uploader.env.env_loader import EnvLoader
from zephyr_uploader.zephyr_uploader.zephyr_service import ZephyrService
from zephyr_uploader.zephyr_uploader.zephyr_uploader import ZephyrUploader
from .constants.exit_constants import ExitConstants
from .model.zephyr_config import ZephyrConfig
from .constants.cli_constants import CliConstants


@click.command()
@click.option('--username', help='The username used to log in Jira. E.g. auto-robot')
@click.option('--password', help='The password used to log in Jira. E.g. passw0rd123!')
@click.option('--jiraUrl', help='The jira url REST endpoint used to submit the results, including the last /. '
                                'E.g. http://jira.yourcompany.com/rest/')
@click.option('--projectKey', help='The project key in Jira. E.g. AIP')
@click.option('--releaseVersion', help='The release version. E.g. 1.2-UP2020-4')
@click.option('--testCycle', help='The test cycle. E.g. Regression_Automated')
@click.option('--reportPath', help='The Excel report path on the disk. E.g. Results.xls')
@click.option('--noOfThreads', default=10,
              help='The number of threads to be used to upload the test executions. E.g. 10')
@click.option('--recreateFolder', default=False, help='Recreate the folder under the test cycle or not. '
                                                      'E.g. true. Default: false')
@click.option('--folderName', default="default_" + date.today().strftime("%Y-%m-%d"),
              help='The release version. E.g. centos7-mysql8-SNAPSHOT. Default: default_<current_date>')
@click.option('--executionStatusColumn', default=6, help='The execution status column which contains the keywords '
                                                         'SUCCESS/FAILURE. E.g. 10. Default: 6')
@click.option('--commentsColumn', default=8, help='The comments column, for example the link log the logs for the test.'
                                                  ' E.g. 11. Default: 8')
def cli(username, password, jira_url, project_key, release_version, test_cycle, report_path, no_of_threads,
        recreate_folder, folder_name, execution_status_column, comments_column):
    zephyr_config = EnvLoader.get_zephyr_config_from_env()
    zephyr_config = ZephyrConfig(zephyr_config)

    zephyr_config_cli = {
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

    zephyr_config.override_or_set_default(zephyr_config_cli)
    zephyr_config.validate()

    try:
        sheet = pyexcel.get_sheet(file_name=zephyr_config.get_config().get(CliConstants.REPORT_PATH))
        excel_data = sheet.to_array()
        zephyr_uploader = ZephyrUploader(ZephyrService(zephyr_config))
        zephyr_uploader.upload_jira_zephyr(excel_data=excel_data)
    except Exception as e:
        click.echo(e.__str__())
        exit(ExitConstants.FAILURE)

    exit(ExitConstants.SUCCESS)


if __name__ == "__main__":
    cli()
