'''
@Author: Ofey Chan
@Date: 2020-05-08 20:40:20
@LastEditors: Ofey Chan
@LastEditTime: 2020-05-08 22:50:10
@Description: Test matcher. The total test of our regex machine.
@Reference: 
'''

from matcher import create_matcher
import unittest

class Test_matcher(unittest.TestCase):
    def test_create_matcher(self):
        # single operator
        single_union = create_matcher("a|b")
        self.assertEqual(single_union(""), False)
        self.assertEqual(single_union("a"), True)
        self.assertEqual(single_union("b"), True)
        self.assertEqual(single_union("ab"), False)
        self.assertEqual(single_union("ba"), False)

        single_concatenation = create_matcher("a.b")
        self.assertEqual(single_concatenation(""), False)
        self.assertEqual(single_concatenation("a"), False)
        self.assertEqual(single_concatenation("b"), False)
        self.assertEqual(single_concatenation("ab"), True)
        self.assertEqual(single_concatenation("ba"), False)

        single_closure = create_matcher("a*b")
        self.assertEqual(single_closure(""), False)
        self.assertEqual(single_closure("a"), False)
        self.assertEqual(single_closure("b"), True)
        self.assertEqual(single_closure("ab"), True)
        self.assertEqual(single_closure("aaaaaab"), True)

        # Compound
        union_and_concate1 = create_matcher("(a|b).c")
        self.assertEqual(union_and_concate1(""), False)
        self.assertEqual(union_and_concate1("ac"), True)
        self.assertEqual(union_and_concate1("bc"), True)
        self.assertEqual(union_and_concate1("abc"), False)
        self.assertEqual(union_and_concate1("bac"), False)

        union_and_concate2 = create_matcher("a|b.c")
        self.assertEqual(union_and_concate2(""), False)
        self.assertEqual(union_and_concate2("a"), True)
        self.assertEqual(union_and_concate2("bc"), True)
        self.assertEqual(union_and_concate2("c"), False)
        self.assertEqual(union_and_concate2("abc"), False)
        self.assertEqual(union_and_concate2("bac"), False)

if __name__ == "__main__":
    unittest.main()
