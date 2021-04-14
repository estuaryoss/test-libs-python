from unittest import TestCase

from zephyr_uploader.zephyr_uploader.constants.cli_constants import CliConstants


class ZephyrConfig(TestCase):
    def __init__(self, config={}):
        """
        The config is a dict with all the details
        """
        self.config = config

    def validate(self):
        self.assertIsNot(self.config.get(CliConstants.USERNAME), None)
        self.assertIsNot(self.config.get(CliConstants.PASSWORD), None)
        self.assertIsNot(self.config.get(CliConstants.JIRA_URL), None)
        self.assertIsNot(self.config.get(CliConstants.TEST_CYCLE), None)
        self.assertIsNot(self.config.get(CliConstants.PROJECT_KEY), None)
        self.assertIsNot(self.config.get(CliConstants.RELEASE_VERSION), None)
        self.assertIsNot(self.config.get(CliConstants.REPORT_PATH), None)
        self.assertIsNot(self.config.get(CliConstants.FOLDER_NAME), None)
        self.assertIsNot(self.config.get(CliConstants.NO_OF_THREADS), None)
        self.assertIsNot(self.config.get(CliConstants.RECREATE_FOLDER), None)
        self.assertIsNot(self.config.get(CliConstants.COMMENTS_COLUMN), None)
        self.assertIsNot(self.config.get(CliConstants.EXECUTION_STATUS_COLUMN), None)

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config

    def override_or_set_default(self, zephyr_config):
        if zephyr_config.get(CliConstants.USERNAME) is not None:
            self.zephyr_config[CliConstants.USERNAME] = zephyr_config.get(CliConstants.USERNAME)
        if zephyr_config.get(CliConstants.PASSWORD) is not None:
            self.zephyr_config[CliConstants.PASSWORD] = zephyr_config.get(CliConstants.PASSWORD)
        if zephyr_config.get(CliConstants.JIRA_URL) is not None:
            self.zephyr_config[CliConstants.JIRA_URL] = zephyr_config.get(CliConstants.JIRA_URL)
        if zephyr_config.get(CliConstants.TEST_CYCLE) is not None:
            self.zephyr_config[CliConstants.TEST_CYCLE] = zephyr_config.get(CliConstants.TEST_CYCLE)
        if zephyr_config.get(CliConstants.PROJECT_KEY) is not None:
            self.zephyr_config[CliConstants.PROJECT_KEY] = zephyr_config.get(CliConstants.PROJECT_KEY)
        if zephyr_config.get(CliConstants.RELEASE_VERSION) is not None:
            self.zephyr_config[CliConstants.RELEASE_VERSION] = zephyr_config.get(CliConstants.RELEASE_VERSION)
        if zephyr_config.get(CliConstants.REPORT_PATH) is not None:
            self.zephyr_config[CliConstants.REPORT_PATH] = zephyr_config.get(CliConstants.REPORT_PATH)
        if zephyr_config.get(CliConstants.FOLDER_NAME) is not None:
            self.zephyr_config[CliConstants.FOLDER_NAME] = zephyr_config.get(CliConstants.FOLDER_NAME)
        self.zephyr_config[CliConstants.NO_OF_THREADS] = zephyr_config.get(CliConstants.NO_OF_THREADS) if \
            zephyr_config.get(CliConstants.TESTNO_OF_THREADS_CYCLE) is not None else 10
        self.zephyr_config[CliConstants.RECREATE_FOLDER] = zephyr_config.get(CliConstants.RECREATE_FOLDER) if \
            zephyr_config.get(CliConstants.RECREATE_FOLDER) is not None else False
        self.zephyr_config[CliConstants.EXECUTION_STATUS_COLUMN] = zephyr_config.get(
            CliConstants.EXECUTION_STATUS_COLUMN) if \
            zephyr_config.get(CliConstants.EXECUTION_STATUS_COLUMN) is not None else 6
        self.zephyr_config[CliConstants.COMMENTS_COLUMN] = zephyr_config.get(CliConstants.COMMENTS_COLUMN) if \
            zephyr_config.get(CliConstants.COMMENTS_COLUMN) is not None else 8
