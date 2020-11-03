#!/usr/bin/env python3

import click

__author__ = "Catalin Dinuta"

from fluent import sender

from about import properties
from constants.cli_constants import CLIConstants
from constants.env_constants import EnvConstants
from env.environment import EnvironmentSingleton
from service.fluentd import Fluentd
from utils.io_utils import IOUtils


@click.command()
@click.option('--tag', prompt='tag',
              help='Fluentd tag used to log the message. E.g. regression')
@click.option('--file', prompt='file',
              help='The json file which contains the message(s). E.g. results.json')
@click.option('--fluentd', default=None, help='The fluentd instance location in "ip:port" format. E.g. localhost:24224')
def cli(tag, file, fluentd):
    env = EnvironmentSingleton.get_instance()
    fluentd = fluentd if fluentd is not None else env.get_env_and_virtual_env().get(EnvConstants.FLUENTD_IP_PORT)

    try:
        if fluentd is None:
            raise Exception(
                "Fluentd ip:port location was not detected in command and neither environment variable " + EnvConstants.FLUENTD_IP_PORT + "\n" +
                "Please set option '-fluentd' in command line interface or set the 'FLUENTD_IP_PORT' environment variable \n")
        logger = sender.FluentSender(tag=properties.get('name'), host=fluentd.split(":")[0],
                                     port=int(fluentd.split(":")[1]))
    except Exception as e:
        click.echo("Exception: {}".format(e.__str__()))
        exit(CLIConstants.FAILURE)

    service = Fluentd(logger)

    try:
        message_content = IOUtils.read_dict_from_file(file=file)
        if isinstance(message_content, list):
            for msg in message_content:
                service.emit(tag=tag, msg=msg)
        elif isinstance(message_content, dict):
            service.emit(tag=tag, msg=message_content)
        else:
            raise Exception("Could not deserialize to a List or a Dict")
    except Exception as e:
        click.echo("Exception{}".format(e.__str__()))
        exit(CLIConstants.FAILURE)

    exit(CLIConstants.SUCCESS)


if __name__ == "__main__":
    cli()
