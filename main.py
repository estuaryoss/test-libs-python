# testing purpose
from fluent import sender

from excel_generator.excel_generator.generator import Generator
from fluentd_logger.fluentd_logger.logger import Logger

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
