import concurrent
import time
from datetime import date

from .constants.cli_constants import CliConstants
from .model.execution_status import ExecutionStatus
from .model.test_status import TestStatus


class ZephyrUploader:
    def __init__(self, zephyr_service):
        """
        Zephyr uploader class takes a zephyr config and uploads the results in jira zephyr
        :param zephyr_service:
        """
        self.zephyr_service = zephyr_service
        self.config = self.zephyr_service.get_zephyr_config()

    def upload_jira_zephyr(self, excel_data):
        folder_name_with_timestamp = self.config.get(CliConstants.FOLDER_NAME) + date.today().strftime("%Y-%m-%d")

        project_id = self.zephyr_service.get_project_id_by_key(self.config.get(CliConstants.PROJECT_KEY))
        version_id = self.zephyr_service.get_version_for_project_id(self.config.get(CliConstants.RELEASE_VERSION),
                                                                    project_id=project_id)
        cycle_id = self.zephyr_service.get_cycle_id(self.config.get(CliConstants.TEST_CYCLE), project_id, version_id)
        folder_id = self.zephyr_service.get_folder_id(folder_name=folder_name_with_timestamp, cycle_id=cycle_id,
                                                      project_id=project_id, version_id=version_id)

        if folder_id is not None and self.config.get(CliConstants.RECREATE_FOLDER):
            self.zephyr_service.delete_folder_from_cycle(folder_id)
            time.sleep(5)
            folder_id = self.zephyr_service.create_folder_under_cycle(folder_name_with_timestamp)

        if folder_id is None:
            self.zephyr_service.create_folder_under_cycle(folder_id=folder_id)

        self.__upload_jira_zephyr_concurrent(excel_data=excel_data)

    def __create_and_update_zephyr_execution(self, row):
        jira_id = row[0]
        issue_id = self.zephyr_service.get_issue_by_key(jira_id)
        execution_id = self.zephyr_service.create_new_execution(issue_id)
        if row[self.config.get(CliConstants.EXECUTION_STATUS_COLUMN)] == ExecutionStatus.SUCCESS:
            self.zephyr_service.update_execution(execution_id, TestStatus.PASSED,
                                                 row[self.config.get(CliConstants.COMMENTS_COLUMN)])
        elif row[self.config.get(CliConstants.EXECUTION_STATUS_COLUMN)] == ExecutionStatus.FAILURE:
            self.zephyr_service.update_execution(execution_id, TestStatus.FAILED,
                                                 row[self.config.get(CliConstants.COMMENTS_COLUMN)])
        else:
            self.zephyr_service.update_execution(execution_id, TestStatus.NOT_EXECUTED,
                                                 row[self.config.get(CliConstants.COMMENTS_COLUMN)])

    def __upload_jira_zephyr_concurrent(self, excel_data):
        max_workers = self.config.get(CliConstants.NO_OF_THREADS)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            {executor.submit(self.__create_and_update_zephyr_execution, row): row for row in excel_data}
