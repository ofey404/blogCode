'''
@Author: Ofey Chan
@Date: 2020-05-08 14:23:57
@LastEditors: Ofey Chan
@LastEditTime: 2020-05-08 20:32:52
@Description: Parse regular expression.
@Reference: 
  https://github.com/deniskyashif/regexjs/blob/master/src/parser.js#L1
  https://en.wikipedia.org/wiki/Shunting-yard_algorithm
'''

def parse_regex_to_postfix(exp: str) -> str:
    return to_postfix(insert_explicit_concate_operator(exp))

not_end_of_trunk = [".", "(", "|"]
not_start_of_trunk = [")", ".", "*", "|"]

# Insert . (concatenation operator) in two trunks which have no operators between.
# Trunks:
# 1. character. ab -> a.b
# 2. bracked expression. (!$#)a -> (!$#).a
# 3. The unary operator * together with its operand.  a*b -> a*.b
def insert_explicit_concate_operator(exp: str) -> str:
    output = ""
    for i, token in enumerate(exp):
        output += token
        if token in not_end_of_trunk:
            continue
        
        # If nothing to peek, break.
        if i == len(exp) - 1:
            continue
        peek_next = exp[i+1]

        if peek_next not in not_start_of_trunk:
            output += "."
        
    return output


# Postfix: Read from right to left, imagine a stack that hold operators until
# enough operands are given.

operators = [".", "|", "*"]

parenthesis = ["(", ")"]

precedence = {
    "|": 0,
    ".": 1,
    "*": 2,
}

def to_postfix(explicited_concate_exp: str) -> str:
    def stack_top_is_poppable(stack, token):
        return (len(stack) > 0) and (stack[-1] != "(") and (precedence[stack[-1]] >= precedence[token])

    output = ""
    operator_stack = []
    
    for token in explicited_concate_exp:
        if (token not in operators) and (token not in parenthesis):
            output += token
        if token in operators:
            while stack_top_is_poppable(operator_stack, token):
                output += operator_stack.pop()
            operator_stack.append(token)
        if token == "(":
            operator_stack.append(token)
        if token == ")":
            while (operator_stack[-1] != "("):
                output += operator_stack.pop()
            operator_stack.pop()
        
    while operator_stack:
        output += operator_stack.pop()
        
    return output
    