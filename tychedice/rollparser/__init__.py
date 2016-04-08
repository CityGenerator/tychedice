#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The Roll Parser is the meat of this app."""

import json
import re
import random
from pprint import pprint
class RollParser(object):
    """ RollParser parses roles."""

    pattern = re.compile("""
        ((\d+)?d(\d+))
    """, re.VERBOSE)



#        (
#        ([^:]+:)?           # Label this roll.
#        (
#            (\d+)?d(\d+)        # 4d20
#            ([HL]\d+|[AD])      # Keep the highest 4, Lowest 4, or use adventage/disadvantage
#            (\s*[+-]\s*\d\+)?   # + or - a number
#        [+-]? )+
#        ;?
#        )+ 






    def __init__(self):
        """ Create a Parser Object"""
        self.msg= "I'm a parser!"
    def parse(self, string=""):
        m=self.pattern.match(string);
        pprint(m.group(1))
        result=self.roll( m.group(2), m.group(1) )

        print "parse %s as %s d %s = %s " % (string, m.group(1), m.group(2), sum(result) )
        return "2"

    def roll(self, dice, num=1):
        result=[]
        if num is None:
            num=1
        for i in xrange(int(num)): 
            result.append( random.randint(1,int(dice)) )
        return result
