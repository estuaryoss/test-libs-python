#!/usr/bin/env python3

import click

__author__ = "Catalin Dinuta"

import pyexcel as p

from excel_exporter.constants.cli_constants import CLIConstants
from excel_exporter.constants.env_constants import EnvConstants
from excel_exporter.env.environment import EnvironmentSingleton
from excel_exporter.utils.io_utils import IOUtils


@click.command()
@click.option('--infile', help="The input file to be used for report generator. E.g. results.json")
@click.option('--outfile',
              help="The desired output file name. The default value is 'results.xls'. E.g. Regression_20.xlsx")
def cli(infile, outfile):
    env = EnvironmentSingleton.get_instance()
    infile = infile if infile is not None else env.get_env_and_virtual_env().get(EnvConstants.IN_FILE)
    outfile = outfile if outfile is not None else env.get_env_and_virtual_env().get(EnvConstants.OUT_FILE)

    if infile is None:
        raise Exception(
            "Input file was not detected in command and neither environment variable " + EnvConstants.IN_FILE + "\n" +
            "Please set option '--infile' in command line interface or set the " + EnvConstants.IN_FILE + " environment variable \n")

    if outfile is None:
        raise Exception(
            "Output file was not detected in command and neither environment variable " + EnvConstants.OUT_FILE + "\n" +
            "Please set option '--outfile' in command line interface or set the " + EnvConstants.OUT_FILE + " environment variable \n")

    if "xls" not in outfile and "xlsx" not in outfile:
        raise Exception(f"Unsupported Excel file extension: {outfile}\n")

    io_utils = IOUtils()
    try:
        messages = io_utils.read_dict_from_file(infile)
    except Exception as e:
        click.echo("Exception: {}".format(e.__str__()))
        exit(CLIConstants.FAILURE)

    try:
        if not isinstance(messages, list):
            click.echo(f"The input file {infile} is not list of dicts")
            exit(CLIConstants.FAILURE)
        if isinstance(messages[0], str):
            click.echo(f"The input file {infile} is not list of dicts")
            exit(CLIConstants.FAILURE)
    except Exception as e:
        click.echo("Exception: {}".format(e.__str__()))
        exit(CLIConstants.FAILURE)

    try:
        p.isave_as(records=messages, dest_file_name=outfile)
    except Exception as e:
        click.echo("Exception: {}".format(e.__str__()))
        exit(CLIConstants.FAILURE)

    exit(CLIConstants.SUCCESS)


if __name__ == "__main__":
    cli()
