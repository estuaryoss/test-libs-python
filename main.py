# testing purpose
import pyexcel
from fluent import sender
from excel_generator.generator import Generator
from fluentd_logger.logger import Logger

from zephyr_uploader.zephyr_uploader.cli_constants import CliConstants
from zephyr_uploader.zephyr_uploader.env_loader import EnvLoader
from zephyr_uploader.zephyr_uploader.zephyr_configurer import ZephyrConfigurer
from zephyr_uploader.zephyr_uploader.zephyr_service import ZephyrService
from zephyr_uploader.zephyr_uploader.zephyr_uploader import ZephyrUploader

if __name__ == '__main__':
    # 1. excel generate
    generator = Generator("testResults.json", "Results.xls")
    generator.generate()

    # 2. fluentd logger
    tag = "agent"
    app_label = "api"
    logger = sender.FluentSender(tag=tag, host="localhost", port=24224)
    service = Logger(logger)

    messages = [
        {
            "A".value: "A1",
            "B".value: "B1"
        },
        {
            "C".value: "C1",
            "D".value: "D1"
        }
    ]

    for message in messages:
        service.emit(app_label=app_label, msg=message)

    # 3. zephyr uploader
    zephyr_config_dict = EnvLoader().get_zephyr_config_from_env()
    zephyr_configurer = ZephyrConfigurer(zephyr_config_dict)
    zephyr_configurer.validate()

    try:
        sheet = pyexcel.get_sheet(file_name=zephyr_configurer.get_config().get(CliConstants.REPORT_PATH.value))
        excel_data = sheet.to_array()
        zephyr_uploader = ZephyrUploader(ZephyrService(zephyr_configurer))
        zephyr_uploader.upload_jira_zephyr(excel_data=excel_data)
    except Exception as e:
        print(e.__str__())
