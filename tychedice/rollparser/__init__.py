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

        result = parser.parse( data, 'AllExpressions')
        print "==========================="
        print "Data is: '%s" % (data)
        indent=0
        for expression in result[1]:
            if expression[0] =="Expression":
                print  self.isp(indent)+ "Result: %s" % str(self.parse_expression(expression[3], data, indent+1))
        print "\n\n"



    def isp(self,indent=0):
        return " "*4*indent
    
    def parse_modifier(self,expr, data, indent=0):
        result=0
        start=expr[1]
        stop=expr[2]
        print self.isp(indent)+"Parsing Modifier %s = %s" %( str(expr), data[start:stop] )
        return int(data[start:stop])

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
                print self.isp(indent)+"Vantage Detected"
    
                vstart=expr[3][-1][1]
                vstop=expr[3][-1][2]
                if data[vstart:vstop]=='A':
                    a=random.randint(1,  int(data[start:stop]))
                    b=random.randint(1,  int(data[start:stop]))
                    roll=max(a,b)
                    print self.isp(indent)+"Adv of %s vs %s = %s" %(a,b,roll)
                else:
                    a=random.randint(1,  int(data[start:stop]))
                    b=random.randint(1,  int(data[start:stop]))
                    roll=min(a,b)
                    print self.isp(indent)+"Dis of %s vs %s = %s" %(a,b,roll)
            else:
                roll= random.randint(1,  int(data[start:stop]))
    
            #print self.isp(indent)+"dicetype rolled a %s" % roll
            rolled.append(roll)
            result+=roll
    
        print self.isp(indent)+"Rolled: %s" % rolled
        print self.isp(indent)+"Dice result is: %s" % result
        return result
    
    def parse_value(self,expr,data,indent=0):
        result=0
        print self.isp(indent)+"Parsing Value %s" % str(expr)
        first_field= expr[3][0]
        if first_field[0] == 'Modifier':
            start=first_field[1]
            stop=first_field[2]
            modifier=data[start:stop]
            result= result + int(modifier)
            print self.isp(indent)+"Modifier result is now %s" % result
        elif first_field[0] == 'Dice':
            start=i[1]
            stop=i[2]
            result += self.parse_dice(i,data, indent +1)

        print self.isp(indent)+"*** My %s expr is %s" %(len(expr[3]), str(expr))
        if len(expr[3]) > 2: #field 3 is op, 5 is next value
            operator_field= expr[3][2]
            start=operator_field[1]
            stop=operator_field[2]
            print self.isp(indent)+"found an operator! %s" % data[start:stop]
            
            second_field=expr[3][4]
            second_start=second_field[1]
            second_stop=second_field[2]
            print self.isp(indent)+"found Second Value! %s" % data[second_start:second_stop]

            if data[start:stop] == '+':
                print self.isp(indent)+"Operator is +"
                second_result= self.parse_value(second_field,data, indent + 1)
                print self.isp(indent)+"Result now %s + %s" % (str(result), second_result)
                result= result + second_result
            else:
                print self.isp(indent)+"Operator is -"
                second_result= self.parse_value(second_field,data, indent + 1)
                print self.isp(indent)+"Result now %s - %s" % (str(result), second_result)
                result= result - second_result
        print self.isp(indent)+"Final result is now %s" % str(result)
        return result

    def parse_expression(self,expr, data, indent=0):
        print self.isp(indent)+"Parsing expression %s" % str(expr)
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
    
        pprint(expr)
        print self.isp(indent)+"Expression result is now %s" % result
        return result





