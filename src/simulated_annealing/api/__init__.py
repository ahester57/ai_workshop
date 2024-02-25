""" Application commands common to all interfaces.

"""
from .hello import main as hello
from .anneal import main as anneal

__all__ = ["hello", "anneal"]
