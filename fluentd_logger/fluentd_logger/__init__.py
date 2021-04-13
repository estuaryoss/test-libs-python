"""Send your information in fluentd. Simple fluentd logger
Import the `Logger` class to send the information to fluentd:
    >>> from fluent import sender
    >>> from fluentd_logger.logger import Logger

    >>> tag = "agent"
    >>> app_label = "api"

    >>> logger = sender.FluentSender(tag=tag, host="localhost", port=24224)
    >>> service = Logger(logger)

    >>> messages = [{    "A": "A1",    "B": "B1"  },  {    "C": "C1",    "D": "D1"  }]

    >>> for message in messages:
    >>>     service.emit(app_label=app_label, msg=message)

See https://github.com/estuaryoss/test-libs-python/tree/master/fluentd_logger for more information
"""
