'''
@Author: Ofey Chan
@Date: 2020-05-08 18:42:49
@LastEditors: Ofey Chan
@LastEditTime: 2020-05-08 22:50:50
@Description: Test file of NFA.py
@Reference: 
'''

import unittest

from parser import insert_explicit_concate_operator, to_postfix
from NFA import to_NFA, FiniteAutomata, State, from_epsilon, from_symbol

class Test_DFA(unittest.TestCase):
    def test_print_some_expression(self):
        # GOGOGO = False
        GOGOGO = True
        def print_correspond_NFA(exp):
            print("===================")
            print("exp: {}".format(exp))
            print(to_NFA(to_postfix(insert_explicit_concate_operator(exp))))

        if GOGOGO:
            print_correspond_NFA("a")
            print_correspond_NFA("a*")
            print_correspond_NFA("ab")
            print_correspond_NFA("a|b")


if __name__ == "__main__":
    unittest.main()