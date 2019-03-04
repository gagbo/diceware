#!/usr/bin/env python3
# coding: utf-8
import copy
import pytest
import re
import random

import dice_rolls.diceware_result as dw
import dice_dict.list_to_dict as ltd


@pytest.fixture()
def bundled_dict():
    bundled_path = "data/diceware-fr-5-jets.txt"
    with open(bundled_path, "r") as bundled_dict_file:
        return ltd.create_dictionary(bundled_dict_file)


def test_passphrase_stability(bundled_dict):
    result = dw.DicewareResult(wordsCount=5, systemRand=True, bonusRoll=True)
    result.make_rolls()
    passphrases = []
    passphrases.append(result.password_from_dict(bundled_dict))
    passphrases.append(result.password_from_dict(bundled_dict))
    # No new make_rolls() calls should leave the passphrase stable
    assert passphrases[0] == passphrases[1]
    result.make_rolls()
    passphrases.append(result.password_from_dict(bundled_dict))
    assert passphrases[1] != passphrases[2]


# TODO : make this a lambda to loop over wordsCount ? Or decorator ?
# Or multiple definitions?
def test_passphrase_wordcount(bundled_dict):
    result = dw.DicewareResult(wordsCount=5, systemRand=True, bonusRoll=True)
    result.make_rolls()
    passphrase = result.password_from_dict(bundled_dict)
    m = re.findall(" ", passphrase)
    assert len(m) == 4
    assert len(re.split(r" ", passphrase)) == 5


def test_salt():
    not_salted = dw.DicewareResult(wordsCount=2, systemRand=True, bonusRoll=False)
    salted = dw.DicewareResult(wordsCount=2, systemRand=True, bonusRoll=True)
    not_salted.make_rolls()
    salted.make_rolls()
    assert salted.salt is not None
    assert not_salted.salt is None


def test_non_system_rand():
    stored_results = []
    result = dw.DicewareResult(wordsCount=5, systemRand=False, bonusRoll=True)

    random.seed("Whatever")
    state = random.getstate()

    result.make_rolls()
    stored_results.append(copy.deepcopy(result))
    result.make_rolls()
    stored_results.append(copy.deepcopy(result))

    random.setstate(state)
    result.make_rolls()
    stored_results.append(copy.deepcopy(result))
    assert stored_results[0].rolls != stored_results[1].rolls
    assert stored_results[0].rolls == stored_results[2].rolls


def test_salt_char():
    # Default behaviour
    assert dw.get_salt_char() == ' '
    # Invalid with a 0
    assert dw.get_salt_char(0, 1) == ' '
    assert dw.get_salt_char(1, 0) == ' '
    # Invalid with a 7
    assert dw.get_salt_char(7, 1) == ' '
    assert dw.get_salt_char(1, 7) == ' '
    # Valid hardcoded table to ensure different stuff
    assert dw.get_salt_char(1, 1) == '~'
    assert dw.get_salt_char(1, 2) == '&'
    assert dw.get_salt_char(1, 3) == '+'
    assert dw.get_salt_char(1, 4) == ':'
    assert dw.get_salt_char(1, 5) == '?'
    assert dw.get_salt_char(1, 6) == '4'
    assert dw.get_salt_char(2, 1) == '!'
    assert dw.get_salt_char(2, 2) == '*'
    assert dw.get_salt_char(2, 3) == '['
    assert dw.get_salt_char(2, 4) == ';'
    assert dw.get_salt_char(2, 5) == '/'
    assert dw.get_salt_char(2, 6) == '5'
    assert dw.get_salt_char(3, 1) == '#'
    assert dw.get_salt_char(3, 2) == '('
    assert dw.get_salt_char(3, 3) == ']'
    assert dw.get_salt_char(3, 4) == '"'
    assert dw.get_salt_char(3, 5) == '0'
    assert dw.get_salt_char(3, 6) == '6'
    assert dw.get_salt_char(4, 1) == '$'
    assert dw.get_salt_char(4, 2) == ')'
    assert dw.get_salt_char(4, 3) == '\\'
    assert dw.get_salt_char(4, 4) == '\''
    assert dw.get_salt_char(4, 5) == '1'
    assert dw.get_salt_char(4, 6) == '7'
    assert dw.get_salt_char(5, 1) == '%'
    assert dw.get_salt_char(5, 2) == '-'
    assert dw.get_salt_char(5, 3) == '{'
    assert dw.get_salt_char(5, 4) == '<'
    assert dw.get_salt_char(5, 5) == '2'
    assert dw.get_salt_char(5, 6) == '8'
    assert dw.get_salt_char(6, 1) == '^'
    assert dw.get_salt_char(6, 2) == '='
    assert dw.get_salt_char(6, 3) == '}'
    assert dw.get_salt_char(6, 4) == '>'
    assert dw.get_salt_char(6, 5) == '3'
    assert dw.get_salt_char(6, 6) == '9'
