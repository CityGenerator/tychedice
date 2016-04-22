#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The Roll Parser is the meat of this app."""

import random
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
        breakdowns = []
        for expression in expr[1]:
            if expression[0] == "Expression":
                [result, breakdown] = self.parse_expression(expression[3], data)
                results.append(str(result))
                breakdowns.append(str(breakdown))

        resultstring='; '.join(results)
        breakdownstring='; '.join(breakdowns)
        return [resultstring, breakdownstring]


    def parse_modifier(self, expr, data):
        """ Parse a simple modifier"""
        start = expr[1]
        stop = expr[2]
        modifier =  int(data[start:stop])
        return [modifier, modifier]

    def parse_op(self, expr, data):
        """ Parse an operator, which is limited to returning a +1 or -1 multiplier"""
        start = expr[1]
        stop = expr[2]
        operator = data[start:stop]
        if operator == '+':
            return [1, operator]
        else:
            return [-1, operator]

    def parse_dice(self, expr, data):
        """ Parse a dice structure"""
        result = 0
        rolled = []
        dicecount = 1
        breakdowns=[]
        start = expr[3][0][1]
        stop = expr[3][0][2]
        if data[start:stop] != '':
            dicecount = int(data[start:stop])

        start = expr[3][1][1]
        stop = expr[3][1][2]
        for _ in range(0, dicecount):
            roll = 0
            breakdown = ''
            if expr[3][-1][0] == 'Vantage':

                vstart = expr[3][-1][1]
                vstop = expr[3][-1][2]
                if data[vstart:vstop] == 'A':
                    a = random.randint(1, int(data[start:stop]))
                    b = random.randint(1, int(data[start:stop]))
                    roll = max(a, b)
                    breakdown='Adv('+str(a)+', '+str(b)+')='+str(roll)
                else:
                    a = random.randint(1, int(data[start:stop]))
                    b = random.randint(1, int(data[start:stop]))
                    roll = min(a, b)
                    breakdown='Dis('+str(a)+', '+str(b)+')='+str(roll)
            else:
                roll = random.randint(1, int(data[start:stop]))
                breakdown=roll

            rolled.append(roll)
            breakdowns.append(str(breakdown))
            result += roll

        breakdownstring='('+ ', '.join(breakdowns)+')'
        return [result, breakdownstring]

    def parse_value(self, expr, data):
        """ Parse a list of values which may include modifiers, operatiors and dice."""
        result = 0
        textresults=[]
        last_op = 1
        last_op_text = ''
        for i in expr[3]:
            textstring=''
            if i[0] == 'Modifier':
                [modifier, textstring]=self.parse_modifier(i, data)
                result = result + last_op * modifier
            elif i[0] == 'Operator':
                [last_op, textstring] = self.parse_op(i, data)
            elif i[0] == 'Dice':
                [dice, textstring] = self.parse_dice(i, data)
                result = result + last_op * dice
            textresults.append(str(textstring))
        finaltext= ' '.join(textresults)
        return [result,finaltext]

    def parse_expression(self, expr, data):
        """ Parse a full expression with optional label."""
        result = ""
        textstrings=[]
        for i in expr:
            textstring=''
            if i[0] == 'Label':
                start = i[1]
                stop = i[2]
                labeltext=data[start:stop] + " "
                result += labeltext
                textstring = labeltext
            elif i[0] == 'Value':
                start = i[1]
                stop = i[2]
                [value, textstring]=self.parse_value(i, data)
                result += str(value)
            textstrings.append(textstring)
        finaltext=' '.join(textstrings)
        return [result, finaltext]

