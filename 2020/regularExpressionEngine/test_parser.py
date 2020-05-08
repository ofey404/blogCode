'''
@Author: Ofey Chan
@Date: 2020-05-08 14:28:50
@LastEditors: Ofey Chan
@LastEditTime: 2020-05-08 22:47:56
@Description: Test file of parser.py
@Reference: 
'''

import unittest

from parser import insert_explicit_concate_operator, to_postfix

class Test_parser(unittest.TestCase):
    def test_insert_explicit_concate_operator(self):
        self.assertEqual(insert_explicit_concate_operator(""), "")
        
        # Simple
        self.assertEqual(insert_explicit_concate_operator("ab"), "a.b")
        self.assertEqual(insert_explicit_concate_operator("abc"), "a.b.c")

        # For brackets
        self.assertEqual(insert_explicit_concate_operator("(ab)c"), "(a.b).c")

        # Shouldn't touch other operators
        self.assertEqual(insert_explicit_concate_operator("a|b"), "a|b")
        self.assertEqual(insert_explicit_concate_operator("a.b"), "a.b")
        self.assertEqual(insert_explicit_concate_operator("a*"), "a*")
        self.assertEqual(insert_explicit_concate_operator("a*b"), "a*.b")
        self.assertEqual(insert_explicit_concate_operator("ab*"), "a.b*")
        self.assertEqual(insert_explicit_concate_operator("a*b"), "a*.b")

        # Compound operators
        self.assertEqual(insert_explicit_concate_operator("a*|b"), "a*|b")
        self.assertEqual(insert_explicit_concate_operator("(a|bc)d"), "(a|b.c).d")
        self.assertEqual(insert_explicit_concate_operator("(a|bc)*d"), "(a|b.c)*.d")

    def test_to_postfix(self):
        self.assertEqual(to_postfix("a"), "a")

        # Simple
        self.assertEqual(to_postfix("a.b"), "ab.")
        self.assertEqual(to_postfix("a|b"), "ab|")
        self.assertEqual(to_postfix("a*"), "a*")

        # Compound
        self.assertEqual(to_postfix("a.b|c"), "ab.c|")
        self.assertEqual(to_postfix("a.b*"), "ab*.")
        self.assertEqual(to_postfix("a*.b"), "a*b.")

        self.assertEqual(to_postfix("a|b.c"), "abc.|")

        # With bracket
        self.assertEqual(to_postfix("a.(b.c)"), "abc..")
        self.assertEqual(to_postfix("a.(b|c)"), "abc|.")
        self.assertEqual(to_postfix("(a.b)*.c"), "ab.*c.")




if __name__ == "__main__":
    unittest.main()