#!/usr/bin/env python3
# coding: utf-8
""" diceware : generate passwords with diceware method
"""
import argparse
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


def create_passphrase(**kwargs):
    """ Create a passphrase using forwarded kwargs arguments to Diceware simulator."""
    result = dw.DicewareResult(**kwargs)
    result.make_rolls()
    return result


if __name__ == "__main__":
    print_entropy_help(sys.stderr)
    p = argparse.ArgumentParser()
    p.add_argument("wordlist", default="data/diceware-fr-5-jets.txt")
    p.add_argument("wordsCount", type=int)
    p.add_argument("--no-salt", dest="bonusRoll", action="store_false", default=True)
    p.add_argument(
        "--no-crypto-rand", dest="systemRand", action="store_false", default=True
    )
    args = p.parse_args()

    with open(args.wordlist, "r") as file_list:
        diceware_dict = list_to_dict.create_dictionary(file_list)

    # Remove the wordlist argument from the namespace, so vars(args)
    # is forwardable to the create_passphrase function, which has
    # the same interface as the DicewareResult constructor.
    vars(args).pop("wordlist", None)

    print("Generation parameters : {}".format(args), file=sys.stderr)
    test_value = create_passphrase(**vars(args))
    print(test_value, file=sys.stderr)
    print(test_value.password_from_dict(diceware_dict))
