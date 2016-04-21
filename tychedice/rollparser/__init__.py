#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The Roll Parser is the meat of this app."""

import random
from pprint import pprint
from simpleparse.parser import Parser

class RollParser(object):
    """ RollParser parses roles."""

    declaration = '''
        ws :=[ \t]*
        Vantage := [AD]
        HiLoCount := [0-9]+
        HiLo := ([HL],HiLoCount)?
        DiceCount :=([0-9]+)*
        DiceType :=[0-9]+
        Operator := [+-]
        Dice := DiceCount,[d],DiceType,(Vantage/HiLo)
        Label := [a-zA-Z0-9_ .?)(!@-]+,[:]
        Modifier := Operator?,[0-9]+
        Value := (Dice/Modifier),(ws,Operator,ws,(Dice/Modifier))*
        Expression := (Label)?,ws,Value
        AllExpressions := Expression,ws,([;],ws,Expression?)?
        '''

    def __init__(self):
        """ Create a Parser Object"""

    def parse(self, data=""):
        ''' Primary Parsing method '''
        parser = Parser(self.declaration)
        expr = parser.parse(data, 'AllExpressions')
        results = []
        #print "==========================="
        #print "Data is: '%s" % (data)
        for expression in expr[1]:
            if expression[0] == "Expression":
                results.append(str(self.parse_expression(expression[3], data)))

        return '; '.join(results)


    def parse_modifier(self, expr, data):
        """ Parse a simple modifier"""
        start = expr[1]
        stop = expr[2]
        return int(data[start:stop])

    def parse_op(self, expr, data):
        """ Parse an operator, which is limited to returning a +1 or -1 multiplier"""
        start = expr[1]
        stop = expr[2]
        if data[start:stop] == '+':
            return 1
        else:
            return -1

    def parse_dice(self, expr, data):
        """ Parse a dice structure"""
        result = 0
        rolled = []
        dicecount = 1

        start = expr[3][0][1]
        stop = expr[3][0][2]
        if data[start:stop] != '':
            dicecount = int(data[start:stop])

        start = expr[3][1][1]
        stop = expr[3][1][2]
        for _ in range(0, dicecount):
            roll = 0
            if expr[3][-1][0] == 'Vantage':

                vstart = expr[3][-1][1]
                vstop = expr[3][-1][2]
                if data[vstart:vstop] == 'A':
                    a = random.randint(1, int(data[start:stop]))
                    b = random.randint(1, int(data[start:stop]))
                    roll = max(a, b)
                else:
                    a = random.randint(1, int(data[start:stop]))
                    b = random.randint(1, int(data[start:stop]))
                    roll = min(a, b)
            else:
                roll = random.randint(1, int(data[start:stop]))

            rolled.append(roll)
            result += roll

        return result

    def parse_value(self, expr, data):
        """ Parse a list of values which may include modifiers, operatiors and dice."""
        result = 0
        last_op = 1
        for i in expr[3]:
            if i[0] == 'Modifier':
                result = result + last_op * self.parse_modifier(i, data)
            elif i[0] == 'Operator':
                last_op = self.parse_op(i, data)
            elif i[0] == 'Dice':
                result = result + last_op * self.parse_dice(i, data)
        return result

    def parse_expression(self, expr, data):
        """ Parse a full expression with optional label."""
        result = ""
        for i in expr:
            if i[0] == 'Label':
                start = i[1]
                stop = i[2]
                result += data[start:stop] + " "
            elif i[0] == 'Value':
                start = i[1]
                stop = i[2]
                result += str(self.parse_value(i, data))

        return result

