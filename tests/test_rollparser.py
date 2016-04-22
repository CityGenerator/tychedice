#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Fully test this module's functionality."

from tychedice.rollparser import RollParser
import unittest2 as unittest
from simpleparse.parser import Parser
from pprint import pprint
#import fixtures


class Test_RollParser(unittest.TestCase):
    """ Test the RollParser Class"""
    def setUp(self):
        """ Set up the required fixtures """
        self.rp=RollParser()
    def tearDown(self):
        """ Clean up any changes from the last run. """
        self.rp=None

    def test_parse_modifier(self):
        data='2-33'

        modifier = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][0]
        #print "My TopLevel modifier is %s" % str(modifier)
        [result, textstring]=self.rp.parse_modifier( modifier, data)
        self.assertEqual(2, result )
        self.assertEqual(2, textstring )
       
        modifier = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][4]
        #print "My TopLevel modifier is %s" % str(modifier)
        [result, textstring]=self.rp.parse_modifier( modifier, data)
        self.assertEqual(33, result )
        self.assertEqual(33, textstring )

    def test_parse_dice (self):
        data="d4"
        dice = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][0]
        #print "My TopLevel dice is %s" % str(dice)
    
        [result, textstring]=self.rp.parse_dice( dice, data)
        self.assertGreater(5, result )
        self.assertLess(0, result )
        self.assertRegexpMatches(textstring, '\(\d\)' )

        
        data="d20"
        dice = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][0]
        [result, textstring]=self.rp.parse_dice( dice, data)
        self.assertGreater(21, result )
        self.assertLess(0, result )
        self.assertRegexpMatches(textstring, '\(\d\d?\)' )

        data="20d6"
        dice = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][0]
        [result, textstring]=self.rp.parse_dice( dice, data)
        self.assertGreater(121, result )
        self.assertLess(19, result )
        self.assertRegexpMatches(textstring, '\('+'\d, '*19+'\d\)' ) # match 19 \d, followed by the 20th \d.
        
        data="1d20A"
        expr=('Dice', 0, 5, [('DiceCount', 0, 1, []), ('DiceType', 2, 4, None), ('Vantage', 4, 5, None)])
        [result, textstring]=self.rp.parse_dice( expr, data)
        self.assertGreater(21, result )
        self.assertLess(0, result )
        self.assertRegexpMatches(textstring, 'Adv\(\d+, \d+\)=\d+' )

        data="1d20D"
        expr=('Dice', 0, 5, [('DiceCount', 0, 1, []), ('DiceType', 2, 4, None), ('Vantage', 4, 5, None)])
        [result, textstring]=self.rp.parse_dice( expr, data)
        self.assertGreater(21, result )
        self.assertLess(0, result )
        self.assertRegexpMatches(textstring, 'Dis\(\d+, \d+\)=\d+' )


    def test_parse_op(self):
        data="3+4"
        op = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][2]
        #print "initial op is"
        #pprint(op)
        [result, textstring]=self.rp.parse_op( op, data)
        self.assertEqual(1, result )
        self.assertEqual(textstring, '+' )

        data="3-4"
        op = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][2]
        [result, textstring]=self.rp.parse_op( op, data)
        self.assertEqual(-1, result )
        self.assertEqual(textstring, '-' )


    def test_parse_value (self):
        data="3+4"
        value = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        [result, textstring]=self.rp.parse_value( value, data)
        self.assertEqual(7, result )
        self.assertEqual(textstring, '3  +  4' )

        data="10-3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        [result, textstring]=self.rp.parse_value( expr, data)
        self.assertEqual(7, result )
        self.assertEqual(textstring, '10  -  3' )

        data="10-3-8"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        #print "initial valueexpression is"
        #pprint(expr)
        [result, textstring]=self.rp.parse_value( expr, data)
        self.assertEqual(-1, result )
        self.assertEqual(textstring, '10  -  3  -  8' )

        data="1d20+3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        [result, textstring]=self.rp.parse_value( expr, data)
        self.assertGreater(24, result )
        self.assertLess(3, result )
        self.assertRegexpMatches(textstring, '\(\d+\)  \+  3' )

        data="1d2+3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        [result, textstring]=self.rp.parse_value( expr, data)
        self.assertGreater(6, result )
        self.assertLess(3, result )
        self.assertRegexpMatches(textstring, '\(\d\)  \+  3' )

        data="1d6+1d8"
        value = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        #print "My TopLevel Value is %s" % str(value)
        [result, textstring]=self.rp.parse_value( value, data)
        self.assertGreater(15, result )
        self.assertLess(1, result )
        self.assertRegexpMatches(textstring, '\(\d\)  \+  \(\d\)' )

    def test_parse_Expression (self):
        data="Attack: 1d20+3+10"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3]
        #print "Testing Expression %s" % str(expr)
        [result, textstring]=self.rp.parse_expression( expr, data)
        self.assertGreater("Attack: 34", result )
        self.assertLess("Attack: 13", result )
        self.assertRegexpMatches(textstring, 'Attack:   \(\d+\)  \+  \d  \+  \d' )

        data="Damage: 1d2+3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3]
        [result, textstring]=self.rp.parse_expression( expr, data)
        self.assertGreater("Damage: 6", result )
        self.assertLess("Damage: 3", result )
        self.assertRegexpMatches(textstring, 'Damage:   \(\d+\)  \+  \d' )


    def test_full_parser(self):

        [result, textstring]=self.rp.parse('2-10')
        self.assertEqual(-8, int(result) )
        self.assertRegexpMatches(textstring, '2  -  10' )
    
        [result, textstring]=self.rp.parse('d4')
        self.assertGreater(5, int(result) )
        self.assertLess(0, int(result) )
        self.assertRegexpMatches(textstring, '\([1-4]\)' )

        [result, textstring]=self.rp.parse('20d6')
        self.assertGreater(121, int(result) )
        self.assertLess(19, int(result) )
        self.assertRegexpMatches(textstring, '\(([1-6], ){19}[1-6]\)' ) #Match 20 total numbers

        [result, textstring]=self.rp.parse('1d20A')
        self.assertGreater(21, int(result) )
        self.assertLess(0, int(result) )
        self.assertRegexpMatches(textstring, '\(Adv\(\d+, \d+\)=\d+\)' )

        [result, textstring]=self.rp.parse('1d20D')
        self.assertGreater(21, int(result) )
        self.assertLess(0, int(result) )
        self.assertRegexpMatches(textstring, '\(Dis\(\d+, \d+\)=\d+\)' )

        [result, textstring]=self.rp.parse('2d8+2')
        self.assertGreater(19, int(result) )
        self.assertLess(3, int(result) )
        self.assertRegexpMatches(textstring, '\([1-8], [1-8]\)  \+  2' )

        [result, textstring]=self.rp.parse('1d20A+2')
        self.assertGreater(23, int(result) )
        self.assertLess(2, int(result) )
        self.assertRegexpMatches(textstring, '^ \(Adv\(\d+, \d+\)=\d+\)  \+  2$' )

        [result, textstring]=self.rp.parse('1d20D-1')
        self.assertGreater(20, int(result) )
        self.assertLess(-1, int(result) )
        self.assertRegexpMatches(textstring, '^ \(Dis\(\d+, \d+\)=\d+\)  -  1$' )

        [result, textstring]=self.rp.parse('1d8+3d6')
        self.assertGreater(27, int(result) )
        self.assertLess(3, int(result) )

        [result, textstring]=self.rp.parse('1d8-0+3d6-3')
        self.assertGreater(24, int(result) )
        self.assertLess(0, int(result) )

        [result, textstring]=self.rp.parse('1d6+2d6+1d4')
        self.assertGreater(23, int(result) )
        self.assertLess(3, int(result) )

        [result, textstring]=self.rp.parse('1d6+2d6+1d4-2')
        self.assertGreater(21, int(result) )
        self.assertLess(1, int(result) )

        [result, textstring]=self.rp.parse('perception check: 1d6A+2')
        self.assertGreater('perception check: 9', result )
        self.assertLess('perception check: 2', result )

        [result, textstring]=self.rp.parse('save vs. spell: 1d6+1')
        self.assertGreater('save vs. spell: 8', result )
        self.assertLess('save vs. spell: 1', result )

#        [result, textstring]=self.rp.parse('stat roll: 4d6H3')

        [result, textstring]=self.rp.parse('Attack: 1d20+4 ; Damage: 1d6+1d4-1')
        parts=result.split(' ')
        self.assertEqual('Attack:', parts[0])
        self.assertGreater(25, int(parts[1][0:-1]) )
        self.assertLess(4, int(parts[1][0:-1]) )


        self.assertEqual('Damage:', parts[2])
        self.assertGreater(10, int(parts[3]) )
        self.assertLess(0, int(parts[3]) )


