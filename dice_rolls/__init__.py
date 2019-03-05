#!/usr/bin/env python3
# coding: utf-8
"""Importing the dice_rolls module will seed the pseudo random number generator
with datetime.now(), just in case."""
import datetime
import random

random.seed(datetime.datetime.now())
