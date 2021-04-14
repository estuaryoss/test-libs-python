from .constants.cli_constants import CliConstants


class ZephyrUploader:
    def __init__(self, zephyr_service):
        """
        Zephyr uploader class takes a zephyr config and uploads the results in jira zephyr
        :param zephyr_service:
        """
        self.zephyr_service = zephyr_service
        self.config = self.zephyr_service.get_zephyr_config()

    def upload_jira_zephyr(self, excel_data):
        folder_id = self.zephyr_service.get_folder_id()

        if folder_id is not None and self.config.get(CliConstants.RECREATE_FOLDER):
            # TODO
            pass

        if folder_id is None:
            # TODO
            pass

        for row in excel_data:
            pass
            # self.zephyr.Create_Folder_under_cycle(self.config.get(CliConstants.TEST_CYCLE),
            #                                       self.config.get(CliConstants.FOLDER_NAME))
            # # self.zephyr.createTestCycle(<CYCLE_NAME>, <startdate>, <enddate>) [dates should be in mm/dd/yy]
            # # self.zephyr.AddTestCasesToCycle(<TEST-CASE-LABEL>, <CYCLE_NAME>, <FOLDER_NAME>)
            # if row[self.config.get(CliConstants.EXECUTION_STATUS_COLUMN)] == ExecutionStatus.SUCCESS:
            #     self.zephyr.updateExecution(row[0], TestStatus.PASSED,
            #                                 row[self.config.get(CliConstants.COMMENTS_COLUMN)])
            # elif row[self.config.get(CliConstants.EXECUTION_STATUS_COLUMN)] == ExecutionStatus.FAILURE:
            #     self.zephyr.updateExecution(row[0], TestStatus.FAILED,
            #                                 row[self.config.get(CliConstants.COMMENTS_COLUMN)])
            # else:
            #     self.zephyr.updateExecution(row[0], TestStatus.NOT_EXECUTED,
            #                                 row[self.config.get(CliConstants.COMMENTS_COLUMN)])
