import distutils

from .environment import EnvironmentSingleton
from ..constants.cli_constants import CliConstants
from ..model.zephyr_config import ZephyrConfig


class EnvLoader:
    __env = EnvironmentSingleton.get_instance().get_env_and_virtual_env()

    @staticmethod
    def get_zephyr_config_from_env():
        zephyr_config = ZephyrConfig()

        if EnvLoader.__env.get(CliConstants.USERNAME) is not None:
            zephyr_config[CliConstants.USERNAME] = EnvLoader.__env.get(CliConstants.USERNAME)

        if EnvLoader.__env.get(CliConstants.PASSWORD) is not None:
            zephyr_config[CliConstants.PASSWORD] = EnvLoader.__env.get(CliConstants.PASSWORD)

        if EnvLoader.__env.get(CliConstants.JIRA_URL) is not None:
            zephyr_config[CliConstants.JIRA_URL] = EnvLoader.__env.get(CliConstants.JIRA_URL)

        if EnvLoader.__env.get(CliConstants.PROJECT_KEY) is not None:
            zephyr_config[CliConstants.PROJECT_KEY] = EnvLoader.__env.get(CliConstants.PROJECT_KEY)

        if EnvLoader.__env.get(CliConstants.RELEASE_VERSION) is not None:
            zephyr_config[CliConstants.RELEASE_VERSION] = EnvLoader.__env.get(CliConstants.RELEASE_VERSION)

        if EnvLoader.__env.get(CliConstants.TEST_CYCLE) is not None:
            zephyr_config[CliConstants.TEST_CYCLE] = EnvLoader.__env.get(CliConstants.TEST_CYCLE)

        if EnvLoader.__env.get(CliConstants.REPORT_PATH) is not None:
            zephyr_config[CliConstants.REPORT_PATH] = EnvLoader.__env.get(CliConstants.REPORT_PATH)

        if EnvLoader.__env.get(CliConstants.FOLDER_NAME) is not None:
            zephyr_config[CliConstants.FOLDER_NAME] = EnvLoader.__env.get(CliConstants.FOLDER_NAME)

        if EnvLoader.__env.get(CliConstants.NO_OF_THREADS) is not None:
            zephyr_config[CliConstants.NO_OF_THREADS] = int(EnvLoader.__env.get(CliConstants.NO_OF_THREADS))

        if EnvLoader.__env.get(CliConstants.RECREATE_FOLDER) is not None:
            zephyr_config[CliConstants.RECREATE_FOLDER] = bool(
                distutils.util.strtobool(EnvLoader.__env.get(CliConstants.RECREATE_FOLDER)))

        return zephyr_config
