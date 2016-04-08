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

    def test_random_simple_rolls(self):
        """ test a random roll. """
        for x in range(0,10):
            result=self.rp.parse("d20")
            self.assertGreater(21, int(result))
            self.assertLess(0, int(result))

        for x in range(0,10):
            result=self.rp.parse("1d20")
            self.assertGreater(21, int(result))
            self.assertLess(0, int(result))

        for x in range(0,4):
            result=self.rp.parse("2d20")
            self.assertGreater(41, int(result))
            self.assertLess(0, int(result))


    def test_multi_rolls(self):
        result=self.rp.parse("1d8+3d6+1d4")
        self.assertGreater(25, int(result))
        self.assertLess(0, int(result))

    def test_additions(self):
        result=self.rp.parse("1d6+10 +2 - 4")
        self.assertGreater(15, int(result))
        self.assertLess(0, int(result))


