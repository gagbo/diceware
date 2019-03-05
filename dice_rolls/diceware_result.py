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

    def __init__(self, words_count=5, system_rand=True, bonus_roll=True):
        """ Constructor of a Diceware Result
        words_count is the number of words in the passphrase
        system_rand asks to use system true random instead of pseudo-random
        bonus_roll asks for one more roll to salt the passphrase with a symbol
        """
        self.words_count = words_count
        self.system_rand = system_rand
        self.bonus_roll = bonus_roll
        self.rolls = None
        self.salt = None
        self.random_generator = None

    def make_rolls(self):
        """ make_rolls fills self.rolls with dice throws
        These 'rolls' which are really 5-uples are the basis for generating
        the true passphrase using a dictionary
        """
        self.rolls = self.generate_rolls()
        self.ensure_random_generator()

        if self.bonus_roll:
            self.salt = roll_5_dice(self.random_generator)
            while self.salt[0] > self.words_count:
                self.salt = roll_5_dice(self.random_generator)
        else:
            self.salt = None

    def generate_rolls(self):
        """ generate_rolls generates a rolls-uple of 5-uple of [1,6] integers
        """
        self.ensure_random_generator()

        result = []
        for _ in range(self.words_count):
            result.append(roll_5_dice(self.random_generator))
        return tuple(result)

    def ensure_random_generator(self):
        """ Create a random generator attribute if not created yet."""
        if hasattr(self, "random_generator") and self.random_generator is not None:
            return

        if self.system_rand:
            self.random_generator = random.SystemRandom()
        else:
            self.random_generator = random.Random()

    def __str__(self):
        """ Method called for str(self) and print(self)
        Useful for debugging purposes
        """
        string = "Diceware Result : {} words with {} generator\n".format(
            self.words_count, "system" if self.system_rand else "pseudo"
        )
        for i in range(self.words_count):
            string += "Word {} : {}\n".format(i + 1, self.rolls[i])

        if self.bonus_roll:
            string += "Salt : {}\n".format(self.salt)

        return string[:-1]

    def key_from_word(self, i):
        """ Transforms self.rolls[i] in an integer.
        It should be used to obtain the key for
        the words dictionary (Diceware list)
        """
        roll = self.rolls[i]
        result = (
            roll[0] * 10000 + roll[1] * 1000 + roll[2] * 100 + roll[3] * 10 + roll[4]
        )
        return result

    def password_from_dict(self, diceware_dict):
        """ Returns the password as a string
        The string is generated with this instance and diceware_dict param
        diceware_dict must be a dictionary indexed with integers representing
           the rolls concatenated
        """
        result = ""
        # Prepare salting the correct word if relevant
        if self.bonus_roll:
            target_word_index = self.salt[0] - 1

        for i in range(self.words_count):
            new_word = list(diceware_dict[self.key_from_word(i)])
            # Salting
            if self.bonus_roll and i == target_word_index:
                target_char = min(self.salt[1], len(new_word))
                replace_char = get_salt_char(self.salt[2], self.salt[3])
                new_word[target_char - 1] = replace_char

            result += "".join(new_word)
            result += " "
        result = result[:-1]
        return result


def roll_5_dice(gen):
    """ roll_5_dice generates a 5-uple of integers between 1 and 6 inclusive
    """
    return (
        gen.randint(1, 6),
        gen.randint(1, 6),
        gen.randint(1, 6),
        gen.randint(1, 6),
        gen.randint(1, 6),
    )


def get_salt_char(digit_three=0, digit_four=0):
    """ get_salt_char returns a char to use as additional char from salt
    It takes 2 digits in the range [1,6] as parameters digitThree digitFour.
    If these parameters are not given, then space is returned
    """
    if digit_three < 1 or digit_four < 1 or digit_three > 6 or digit_four > 6:
        return " "

    symbol_table = (
        ("~", "!", "#", "$", "%", "^"),
        ("&", "*", "(", ")", "-", "="),
        ("+", "[", "]", "\\", "{", "}"),
        (":", ";", '"', "'", "<", ">"),
        ("?", "/", "0", "1", "2", "3"),
        ("4", "5", "6", "7", "8", "9"),
    )

    return symbol_table[digit_four - 1][digit_three - 1]
