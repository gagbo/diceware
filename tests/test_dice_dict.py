#!/usr/bin/env python3
# coding: utf-8
import pytest
import math

import dice_dict.list_to_dict


@pytest.fixture
def bundled_dict():
    test_dict_path = "data/diceware-fr-5-jets.txt"
    with open(test_dict_path, "r") as test_dict:
        return dice_dict.list_to_dict.create_dictionary(test_dict)


def test_dictionary_length(bundled_dict):
    assert len(bundled_dict) == math.pow(6, 5)


def test_dictionary_keys(bundled_dict):
    assert bundled_dict[11116] == "---"
    assert bundled_dict[66656] == "zv"
    assert bundled_dict[36411] == "lampe"
    assert 72134 not in bundled_dict
    assert 1111 not in bundled_dict
    assert 111111 not in bundled_dict
