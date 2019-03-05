#!/usr/bin/env python3
# coding: utf-8
""" diceware : generate passwords with diceware method
"""
import argparse
import sys

import dice_dict.list_to_dict as ltd
import dice_rolls.diceware_result as dw


def print_entropy_help(file_desc):
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
        file=file_desc,
    )


def create_passphrase(**kwargs):
    """ Create a passphrase using forwarded kwargs arguments to Diceware simulator."""
    result = dw.DicewareResult(**kwargs)
    result.make_rolls()
    return result


def parse_cli_arguments():
    """Return an argparse.Namespace with relevant command-line parsing."""
    parser = argparse.ArgumentParser()
    parser.add_argument("wordlist", default="data/diceware-fr-5-jets.txt")
    parser.add_argument("words_count", type=int)
    parser.add_argument(
        "--no-salt", dest="bonus_roll", action="store_false", default=True
    )
    parser.add_argument(
        "--no-crypto-rand", dest="system_rand", action="store_false", default=True
    )
    return parser.parse_args()


if __name__ == "__main__":
    print_entropy_help(sys.stderr)

    ARGS = parse_cli_arguments()

    with open(ARGS.wordlist, "r") as file_list:
        DICEWARE_DICT = ltd.create_dictionary(file_list)

    # Remove the wordlist argument from the namespace, so vars(args)
    # is forwardable to the create_passphrase function, which has
    # the same interface as the DicewareResult constructor.
    vars(ARGS).pop("wordlist", None)

    print("Generation parameters : {}".format(ARGS), file=sys.stderr)
    TEST_VALUE = create_passphrase(**vars(ARGS))
    print(TEST_VALUE, file=sys.stderr)
    print(TEST_VALUE.password_from_dict(DICEWARE_DICT))
