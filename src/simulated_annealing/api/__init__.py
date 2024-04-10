""" Application commands common to all interfaces.

"""
from .hello import main as hello
from .anneal import main as anneal
from .convolve import main as convolve
from .svm import main as svm


__all__ = ['hello', 'anneal', 'svm', 'convolve']
