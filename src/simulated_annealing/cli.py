""" Implementation of the command line interface.

https://github.com/mdklatt/cookiecutter-python-app
"""
from argparse import _SubParsersAction, ArgumentParser, Namespace
from inspect import getfullargspec
from os import environ
from typing import Any, Sequence

from . import __version__
from .api import anneal
from .core.config import config
from .core.logger import logger


__all__ = ['main']


def main(argv:Sequence[str]|None=None) -> int:
    """ Execute the application CLI.

    :param argv: argument list to parse (sys.argv by default)
    :type argv: Sequence[str]|None
    :return: exit status
    :rtype: int
    """
    args : Namespace = _args(argv)
    logger.start(args.warn)
    logger.debug('starting execution')
    config.load(args.config, params=environ)
    config.core.config = args.config
    if args.warn:
        config.core.logging = args.warn
    logger.stop()  # clear handlers to prevent duplicate records
    logger.start(config.core.get('logging'))
    command = args.command
    args_dict : dict[str, Any] = vars(args)
    spec = getfullargspec(command)
    if not spec.varkw:
        # No kwargs, remove unexpected arguments.
        args_dict = {key: args_dict[key] for key in args_dict if key in spec.args}
    try:
        result = command(**args_dict)
        #logger.debug(result)
    except RuntimeError as err:
        logger.critical(err)
        return 1
    logger.debug('successful completion')
    return 0


def _args(argv:Sequence[str]|None) -> Namespace:
    """ Parse command line arguments.

    :param argv: argument list to parse
    :type argv: Sequence[str]|None
    :return: The parsed arguments
    :rtype: Namespace
    """
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', action='append',
            help='config file [etc/config.toml]')
    parser.add_argument('-v', '--version', action='version',
            version=f'simulated-annealing {__version__}',
            help='print version and exit')
    parser.add_argument('-w', '--warn', # default not needed due to logger.start having default
            help='logger warning level [WARN]')
    parser.set_defaults(command=None)
    subparsers = parser.add_subparsers(title='subcommands')
    common = ArgumentParser(add_help=False)  # common subcommand arguments
    # common.add_argument('-d', '--draw-graph', default=True, help='visualize graph')
    _anneal(subparsers, common)
    args = parser.parse_args(argv)
    if not args.command:
        # No subcommand was specified.
        parser.print_help()
        raise SystemExit(1)
    if not args.config:
        # Don't specify this as an argument default or else it will always be
        # included in the list.
        args.config = 'etc/config.toml'
    return args


def _anneal(subparsers:_SubParsersAction, common:ArgumentParser) -> None:
    """ CLI adaptor for the api.anneal command.

    :param subparsers: subcommand parsers
    :type subparsers: _SubParsersAction
    :param common: parser for common subcommand arguments
    :type common: ArgumentParser
    """
    parser = subparsers.add_parser('anneal', parents=[common])
    parser.set_defaults(command=anneal)


# Make the module executable.

if __name__ == '__main__':
    try:
        STATUS = main()
    except Exception as _err:
        # Error handler of last resort.
        logger.error(repr(_err))
        logger.critical('shutting down due to fatal error')
        raise  # print stack trace
    raise SystemExit(STATUS)
