#!/usr/bin/env python3
# coding: utf-8
""" diceware : generate passwords with diceware method
"""
# TODO : find the URL of the diceware paper for reference
#    Then it can be pulled for justifying stuff, like the reason for naming
#    the arguments in get_separator digitThree, digitFour

import datetime
import random
import sys


class DicewareResult:
    """ DicewareResult contains all the data from the diceware protocol
        in number + bonus_separator form, so all this object can be used to
        check up the words database.
    """
    def __init__(self, wordsCount=5, systemRand=True, bonusRoll=True):
        self.wordsCount = wordsCount
        self.systemRand = systemRand
        self.bonusRoll = bonusRoll

    def make_rolls(self):
        self.words = generate_rolls(words=self.wordsCount,
                                    systemRand=self.systemRand)
        # TODO : while loop until we get a bonus roll that's correct


def roll_5_dice(gen):
    """ roll_5_dice generates a 5-uple of integers between 1 and 6 inclusive
    """
    return (gen.randint(1, 6),
            gen.randint(1, 6),
            gen.randint(1, 6),
            gen.randint(1, 6),
            gen.randint(1, 6))


def generate_rolls(words=5, systemRand=True):
    """ generate_rolls generates a words-uple of 5-uple of [1,6] integers
    """
    if systemRand:
        random_machine = random.SystemRandom()
    else:
        random_machine = random.Random()

    result = []
    for i in range(words):
        result.append(roll_5_dice(random_machine))
    return tuple(result)


def get_separator(digitThree=0, digitFour=0):
    """ get_separator returns a char to use typically as separator
    It takes 2 digits in the range [1,6] as parameters digitThree digitFour.
    If these parameters are not given, then space is returned
    """
    if digitThree == 0 or digitFour == 0:
        return ' '

    symbol_table = (('~', '!', '#', '$', '%', '^'),
                    ('&', '*', '(', ')', '-', '='),
                    ('+', '[', ']', '\\', '{', '}'),
                    (':', ';', '"', '\'', '<', '>'),
                    ('?', '/', '0', '1', '2', '3'),
                    ('4', '5', '6', '7', '8', '9'))

    return symbol_table[digitFour][digitThree]


def print_entropy_help(fileDesc):
    """ print_entropy_help prints on fileDesc a remainder on word count
    """
    print("Each diceware word brings 12.9 bits of entropy. Therefore :\n"
          "   - 4 words is breakable by ~100 computers.\n"
          "   - 5 words is breakable only by a corporation with large budget\n"
          "   - 6 words seems unbreakeable in the forseeable future, but "
          "may be in the grasp of state-backed attacks\n"
          "   - 7 words is unbreakeable with current state of the art\n"
          "   - 8 words is safe for the times to come\n", file=fileDesc)


if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    print_entropy_help(sys.stdout)
    print(generate_rolls(5))