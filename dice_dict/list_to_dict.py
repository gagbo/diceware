#!/usr/bin/env python3
# coding: utf-8
""" words_list : Utilities to generate a python dictionary from a words list
    The behaviour is undefined if used with a word list which does not use
5-throw lists (with results per word being '11111' to '66666' inclusive with
only digits in 1-6 inclusive)
"""


def create_dictionary(in_file):
    """ Returns a dict from a file handle to a readable diceware words list
    The keys are the 5 rolls concatenated into an integer
    The values are strings with the actual words matching a 5-roll
    """
    words_dict = {}
    for line in in_file:
        words = line.split()
        key = int(words[0])
        value = words[1]
        words_dict[key] = value
    return words_dict
