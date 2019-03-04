#!/usr/bin/env python3
# coding: utf-8
""" diceware : generate passwords with diceware method
"""
import sys

import dice_dict.list_to_dict as list_to_dict
import dice_rolls.diceware_result as dw


def print_entropy_help(fileDesc):
    """ print_entropy_help prints on fileDesc a remainder on word count
    """
    print(
        "Each diceware word brings 12.9 bits of entropy. Therefore :\n"
        "   - 4 words is breakable by ~100 computers.\n"
        "   - 5 words is breakable only by a corporation with large budget\n"
        "   - 6 words seems unbreakeable in the forseeable future, but "
        "may be in the grasp of state-backed attacks\n"
        "   - 7 words is unbreakeable with current state of the art\n"
        "   - 8 words is safe for the times to come\n",
        file=fileDesc,
    )


if __name__ == "__main__":
    print_entropy_help(sys.stdout)
    with open("data/diceware-fr-5-jets.txt", "r") as fr:
        diceware_dict = list_to_dict.create_dictionary(fr)

    print("Default :")
    test_value = dw.DicewareResult()
    test_value.make_rolls()
    print(test_value)
    print(test_value.password_from_dict(diceware_dict))

    print("\nOnly 2 words :")
    test_value_2 = dw.DicewareResult(wordsCount=2)
    test_value_2.make_rolls()
    print(test_value_2)
    print(test_value_2.password_from_dict(diceware_dict))

    print("\nNo salt :")
    test_value_3 = dw.DicewareResult(bonusRoll=False)
    test_value_3.make_rolls()
    print(test_value_3)
    print(test_value_3.password_from_dict(diceware_dict))

    print("\nPseudo random - No Salt - 3 words :")
    test_value_4 = dw.DicewareResult(
        wordsCount=3, systemRand=False, bonusRoll=False)
    test_value_4.make_rolls()
    print(test_value_4)
    print(test_value_4.password_from_dict(diceware_dict))
