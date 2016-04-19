#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The Roll Parser is the meat of this app."""

import random
from simpleparse.parser import Parser
from pprint import pprint

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
        Label := [a-zA-Z0-9_ ]+,[:]
        Modifier := Operator?,[0-9]+
        Value := (Dice/Modifier),(ws,Operator,ws,(Dice/Modifier))*
        Expression := (Label)?,ws,Value
        AllExpressions := Expression,ws,([;],ws,Expression?)?
        '''



    def __init__(self):
        """ Create a Parser Object"""
        self.msg= "I'm a parser!"


    def parse(self, data=""):
        parser = Parser( self.declaration )
        expr = parser.parse( data, 'AllExpressions')
        results=[]
        #print "==========================="
        #print "Data is: '%s" % (data)
        indent=0
        for expression in expr[1]:
            if expression[0] =="Expression":
                results.append(str(self.parse_expression(expression[3], data, indent+1)))
            
        return '; '.join(results)


    def isp(self,indent=0):
        return " "*4*indent
    
    def parse_modifier(self,expr, data, indent=0):
        result=0
        start=expr[1]
        stop=expr[2]
        #print self.isp(indent)+"Parsing Modifier %s = %s" %( str(expr), data[start:stop] )
        return int(data[start:stop])

    def parse_op(self,expr, data, indent=0):
        result=0
        start=expr[1]
        stop=expr[2]
        #print self.isp(indent)+"Parsing operator %s = %s [%s:%s]" %( str(expr), data[start:stop], start, stop )
        if data[start:stop] =='+':
            return 1
        else:
            return -1

    def parse_dice(self,expr,data, indent=0):
        result=0
        rolled=[]
        #print self.isp(indent)+"Parsing dice %s" % str(expr)
        dicecount=1
        #print self.isp(indent)+" value is "+str(expr[3][0])
    
        start=expr[3][0][1]
        stop=expr[3][0][2]
        if data[start:stop] != '':
            dicecount=int(data[start:stop])
    
        start=expr[3][1][1]
        stop=expr[3][1][2]
        for x in range(0,dicecount):
            roll=0
            if expr[3][-1][0] == 'Vantage':
                #print self.isp(indent)+"Vantage Detected"
    
                vstart=expr[3][-1][1]
                vstop=expr[3][-1][2]
                if data[vstart:vstop]=='A':
                    a=random.randint(1,  int(data[start:stop]))
                    b=random.randint(1,  int(data[start:stop]))
                    roll=max(a,b)
                    #print self.isp(indent)+"Adv of %s vs %s = %s" %(a,b,roll)
                else:
                    a=random.randint(1,  int(data[start:stop]))
                    b=random.randint(1,  int(data[start:stop]))
                    roll=min(a,b)
                    #print self.isp(indent)+"Dis of %s vs %s = %s" %(a,b,roll)
            else:
                roll= random.randint(1,  int(data[start:stop]))
    
            #print self.isp(indent)+"dicetype rolled a %s" % roll
            rolled.append(roll)
            result+=roll
    
        #print self.isp(indent)+"Rolled: %s" % rolled
        #print self.isp(indent)+"Dice result is: %s" % result
        return result
    
    def parse_value(self,expr,data,indent=0):
        result=0
        #print self.isp(indent)+"Parse value thing:"+ str(expr[3])
        last_op=1
        for i in expr[3]:
            if i[0] == 'Modifier':
                result = result + last_op*self.parse_modifier(i,data,indent+1)
            elif i[0] == 'Operator':
                last_op = self.parse_op(i,data,indent+1)
            elif i[0] == 'Dice':
                result = result + last_op*self.parse_dice(i,data,indent+1)
        return result

    def parse_expression(self,expr, data, indent=0):
        #print self.isp(indent)+"Parsing expression %s" % str(expr)
        result= ""
        for i in expr:
            if i[0] == 'Label':
                start=i[1]
                stop=i[2]
                result += data[start:stop]+" "
            elif i[0] == 'Value':
                start=i[1]
                stop=i[2]
                result += str(self.parse_value(i,data, indent +1))
    
        #pprint(expr)
        #print self.isp(indent)+"Expression result is now %s" % result
        return result





