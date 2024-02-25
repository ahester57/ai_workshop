""" Implement the hello command.

"""
from ..core.logger import logger


def main(name:str|None="World") -> str:
    """ Execute the command.
    
    :param name: name to use in greeting
    :type name: str|None
    :return: Greeting for the user.
    :rtype: str
    """
    logger.debug("executing hello command")
    return f"Hello, {name}!"
