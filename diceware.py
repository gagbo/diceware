#!/usr/bin/env python3
# coding: utf-8
""" diceware : generate passwords with diceware method
"""
import datetime
import random
import sys


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
        """ make_rolls fills self.words with dice throws
        These 'words' which are really 5-uples are the basis for generating
        the true passphrase using a dictionary
        """
        self.words = generate_rolls(words=self.wordsCount,
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
            string += "Word {} : {}\n".format(i + 1, self.words[i])

        if self.bonusRoll:
            string += "Salt : {}\n".format(self.salt)

        return string[:-1]

    def key_from_word(self, i):
        """ Transforms self.words[i] in an integer.
        It should be used to obtain the key for
        the words dictionary (Diceware list)
        """
        roll = self.words[i]
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
    with open("data/diceware-fr-5-jets.txt", "r") as fr:
        diceware_dict = create_dictionary(fr)

    print("Default :")
    test_value = DicewareResult()
    test_value.make_rolls()
    print(test_value)
    print(test_value.password_from_dict(diceware_dict))

    print("\nOnly 2 words :")
    test_value_2 = DicewareResult(wordsCount=2)
    test_value_2.make_rolls()
    print(test_value_2)
    print(test_value_2.password_from_dict(diceware_dict))

    print("\nNo salt :")
    test_value_3 = DicewareResult(bonusRoll=False)
    test_value_3.make_rolls()
    print(test_value_3)
    print(test_value_3.password_from_dict(diceware_dict))

    print("\nPseudo random - No Salt - 3 words :")
    test_value_4 = DicewareResult(
        wordsCount=3, systemRand=False, bonusRoll=False)
    test_value_4.make_rolls()
    print(test_value_4)
    print(test_value_4.password_from_dict(diceware_dict))
