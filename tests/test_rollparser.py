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
    def test_isp(self):
        self.assertEqual('    ', self.rp.isp(1))
        self.assertEqual(' '*16, self.rp.isp(4))
       

    def test_parse_modifier(self):
        data='2-33'

        modifier = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][0]
        #print "My TopLevel modifier is %s" % str(modifier)
        result=self.rp.parse_modifier( modifier, data)
        self.assertEqual(2, result )
       
        modifier = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][4]
        #print "My TopLevel modifier is %s" % str(modifier)
        result=self.rp.parse_modifier( modifier, data)
        self.assertEqual(33, result )

    def test_parse_dice (self):
        data="d4"
        dice = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][0]
        #print "My TopLevel dice is %s" % str(dice)
    
        result=self.rp.parse_dice( dice, data)
        self.assertGreater(5, result )
        self.assertLess(0, result )

        
        data="d20"
        expr=('Dice', 0, 3, [('DiceCount', 0, 0, []), ('DiceType', 1, 3, None)])
    
        result=self.rp.parse_dice( expr, data)
        self.assertGreater(21, result )
        self.assertLess(0, result )

        data="20d6"
        expr=('Dice', 0, 4, [('DiceCount', 0, 2, []), ('DiceType', 3, 4, None)])
        result=self.rp.parse_dice( expr, data)
        self.assertGreater(121, result )
        self.assertLess(19, result )
        
        data="1d20A"
        expr=('Dice', 0, 5, [('DiceCount', 0, 1, []), ('DiceType', 2, 4, None), ('Vantage', 4, 5, None)])
        result=self.rp.parse_dice( expr, data)
        self.assertGreater(21, result )
        self.assertLess(0, result )

        data="1d20D"
        expr=('Dice', 0, 5, [('DiceCount', 0, 1, []), ('DiceType', 2, 4, None), ('Vantage', 4, 5, None)])
        result=self.rp.parse_dice( expr, data)
        self.assertGreater(21, result )
        self.assertLess(0, result )


    def test_parse_op(self):
        data="3+4"
        op = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1][3][2]
        #print "initial op is"
        #pprint(op)
        result=self.rp.parse_op( op, data)
        self.assertEqual(1, result )


    def test_parse_value (self):
        data="3+4"
        value = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        result=self.rp.parse_value( value, data)
        self.assertEqual(7, result )

        data="10-3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        result=self.rp.parse_value( expr, data)
        self.assertEqual(7, result )

        data="10-3-8"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        #print "initial valueexpression is"
        #pprint(expr)
        result=self.rp.parse_value( expr, data)
        self.assertEqual(-1, result )

        data="1d20+3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        result=self.rp.parse_value( expr, data)
        self.assertGreater(24, result )
        self.assertLess(3, result )

        data="1d2+3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        result=self.rp.parse_value( expr, data)
        self.assertGreater(6, result )
        self.assertLess(3, result )

        data="1d6+1d8"
        value = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3][1]
        #print "My TopLevel Value is %s" % str(value)
        result=self.rp.parse_value( value, data)
        self.assertGreater(15, result )
        self.assertLess(1, result )

    def test_parse_Expression (self):
        data="Attack: 1d20+3+10"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3]
        #print "Testing Expression %s" % str(expr)
        result=self.rp.parse_expression( expr, data)
        self.assertGreater("Attack: 34", result )
        self.assertLess("Attack: 13", result )

        data="damage: 1d2+3"
        expr = Parser( self.rp.declaration ).parse(data,'AllExpressions')[1][0][3]
        result=self.rp.parse_expression( expr, data)
        self.assertGreater("damage: 6", result )
        self.assertLess("damage: 3", result )


    def test_full_parser(self):

        result=self.rp.parse('2-10')
        self.assertEqual(-8, int(result) )
    
        result=self.rp.parse('d4')
        self.assertGreater(5, int(result) )
        self.assertLess(0, int(result) )

        result=self.rp.parse('20d6')
        self.assertGreater(121, int(result) )
        self.assertLess(19, int(result) )

        result=self.rp.parse('1d20A')
        self.assertGreater(21, int(result) )
        self.assertLess(0, int(result) )

        result=self.rp.parse('1d20D')
        self.assertGreater(21, int(result) )
        self.assertLess(0, int(result) )

        result=self.rp.parse('2d8+2')
        self.assertGreater(19, int(result) )
        self.assertLess(3, int(result) )

        result=self.rp.parse('1d20A+2')
        self.assertGreater(23, int(result) )
        self.assertLess(2, int(result) )

        result=self.rp.parse('1d20D-1')
        self.assertGreater(20, int(result) )
        self.assertLess(-1, int(result) )

        result=self.rp.parse('1d8+3d6')
        self.assertGreater(27, int(result) )
        self.assertLess(3, int(result) )

        result=self.rp.parse('1d8-0+3d6-3')
        self.assertGreater(24, int(result) )
        self.assertLess(1, int(result) )

        result=self.rp.parse('1d6+2d6+1d4')
        self.assertGreater(23, int(result) )
        self.assertLess(3, int(result) )

        result=self.rp.parse('1d6+2d6+1d4-2')
        self.assertGreater(21, int(result) )
        self.assertLess(1, int(result) )

        result=self.rp.parse('perception check: 1d6A+2')
        self.assertGreater('perception check: 9', result )
        self.assertLess('perception check: 2', result )

#        result=self.rp.parse('stat roll: 4d6H3')

        result=self.rp.parse('Attack: 1d20+4 ; Damage: 1d6+1d4-1')
        parts=result.split(' ')
        self.assertEqual('Attack:', parts[0])
        self.assertGreater(25, int(parts[1][0:-1]) )
        self.assertLess(4, int(parts[1][0:-1]) )


        self.assertEqual('Damage:', parts[2])
        self.assertGreater(10, int(parts[3]) )
        self.assertLess(0, int(parts[3]) )


