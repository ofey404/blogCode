# Implementing a Regular Expression Engine
For a small training after reading [Introduction to the Theory of Computation](https://www.amazon.com/Introduction-Theory-Computation-Michael-Sipser/dp/113318779X), PART ONE Automata and languages. And Thanks to Denis Kyashif's wonderful Blog [Implementing a Regular Expression Engine](https://deniskyashif.com/2019/02/17/implementing-a-regular-expression-engine/), I adapt his javascript implementation to python.

## Kickstart guide
This project implemented a regular engine in python.

Check three test file to know the usage. `test_NFA.py`, `test_matcher.py` and `test_parser.py`.

The main workhorse function is `matcher.create_matcher`.

```python
from matcher import create_matcher

# Return a matcher function.
union_and_concate = create_matcher("(a|b).c")

union_and_concate("")  # False
union_and_concate("ac")  # True
union_and_concate("bc")  # True
union_and_concate("abc")  # False
union_and_concate("bac")  # False
```

## Overview of implementation
> What this project do?

Mainly can refer to the Denis Kyashif's Blog [Implementing a Regular Expression Engine](https://deniskyashif.com/2019/02/17/implementing-a-regular-expression-engine/)

`parser.py` -> `NFA.py` -> `matcher.py`

Begin with a input of regex string
- Parser do(`parse_regex_to_postfix()`):
    - Insert explicit concate operator(`.`).
    - Turn regex to postfix notation, with [Shunting-yard Algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm#Graphical_illustration)
- Turn postfix regex to NFA(`to_NFA()`):
    - Use Thompson’s Construction to construct NFA, refer to Denis's wonderful blog.
- Build a matcher(`create_matcher`):
    - Follow the automata non-deterministically, step by step.