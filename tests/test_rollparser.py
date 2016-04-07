#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Fully test this module's functionality."

from tychedice.rollparser import RollParser
import unittest2 as unittest
#import fixtures


class Test_RollParser(unittest.TestCase):
    """ Test the RollParser Class"""
    def setUp(self):
        """ Set up the required fixtures """
        self.rp=RollParser()
    def tearDown(self):
        """ Clean up any changes from the last run. """
        self.rp=None

    def test_random_Roll(self):
        """ test a random roll. """
        self.assertEqual("sure, ok.", self.rp.parse('asd'))


