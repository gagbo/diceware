#!/usr/bin/env python3
# coding: utf-8
""" diceware_result : Utilities to generate dice rolls for diceware method.
    The count of rolls per word (currently 5 die per word), is hardcoded in
a few places and behaviour with non 5-throw lists (from '11111' to '66666'
with only 1-6 inclusive digits) is undefined.
"""
import random


class DicewareResult:
    """ DicewareResult contains all the data from the diceware protocol
        in number + bonus_separator form, so all this object can be used to
        check up the words database.
    """

    def __init__(self, wordsCount=5, systemRand=True, bonusRoll=True):
        """ Constructor of a Diceware Result
        wordsCount is the number of words in the passphrase
        systemRand asks to use system true random instead of pseudo-random
        bonusRoll asks for one more roll to salt the passphrase with a symbol
        """
        self.wordsCount = wordsCount
        self.systemRand = systemRand
        self.bonusRoll = bonusRoll

    def make_rolls(self):
        """ make_rolls fills self.rolls with dice throws
        These 'rolls' which are really 5-uples are the basis for generating
        the true passphrase using a dictionary
        """
        self.rolls = generate_rolls(rolls=self.wordsCount,
                                    systemRand=self.systemRand)
        if self.systemRand:
            random_machine = random.SystemRandom()
        else:
            random_machine = random.Random()

        if self.bonusRoll:
            self.salt = roll_5_dice(random_machine)
            while self.salt[0] > self.wordsCount:
                self.salt = roll_5_dice(random_machine)

    def __str__(self):
        """ Method called for str(self) and print(self)
        Useful for debugging purposes
        """
        string = "Diceware Result : {} words with {} generator\n".format(
            self.wordsCount, "system" if self.systemRand else "pseudo")
        for i in range(self.wordsCount):
            string += "Word {} : {}\n".format(i + 1, self.rolls[i])

        if self.bonusRoll:
            string += "Salt : {}\n".format(self.salt)

        return string[:-1]

    def key_from_word(self, i):
        """ Transforms self.rolls[i] in an integer.
        It should be used to obtain the key for
        the words dictionary (Diceware list)
        """
        roll = self.rolls[i]
        result = (roll[0] * 10000 + roll[1] * 1000 +
                  roll[2] * 100 + roll[3] * 10 + roll[4])
        return result

    def password_from_dict(self, diceware_dict):
        """ Returns the password as a string
        The string is generated with this instance and diceware_dict param
        diceware_dict must be a dictionary indexed with integers representing
           the rolls concatenated
        """
        result = ''
        # Prepare salting the correct word if relevant
        if self.bonusRoll:
            target_word_index = self.salt[0] - 1

        for i in range(self.wordsCount):
            new_word = list(diceware_dict[self.key_from_word(i)])
            # Salting
            if self.bonusRoll and i == target_word_index:
                target_char = min(self.salt[1], len(new_word))
                replace_char = get_salt_char(self.salt[2], self.salt[3])
                new_word[target_char - 1] = replace_char

            result += "".join(new_word)
            result += ' '
        result = result[:-1]
        return result


def roll_5_dice(gen):
    """ roll_5_dice generates a 5-uple of integers between 1 and 6 inclusive
    """
    return (gen.randint(1, 6),
            gen.randint(1, 6),
            gen.randint(1, 6),
            gen.randint(1, 6),
            gen.randint(1, 6))


def generate_rolls(rolls=5, systemRand=True):
    """ generate_rolls generates a rolls-uple of 5-uple of [1,6] integers
    """
    if systemRand:
        random_machine = random.SystemRandom()
    else:
        random_machine = random.Random()

    result = []
    for i in range(rolls):
        result.append(roll_5_dice(random_machine))
    return tuple(result)


def get_salt_char(digitThree=0, digitFour=0):
    """ get_salt_char returns a char to use as additional char from salt
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

    return symbol_table[digitFour - 1][digitThree - 1]
