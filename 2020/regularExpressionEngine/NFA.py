'''
@Author: Ofey Chan
@Date: 2020-05-08 14:13:09
@LastEditors: Ofey Chan
@LastEditTime: 2020-05-08 22:16:43
@Description: Non-deterministic finite automata. 
@Reference:
  https://deniskyashif.com/2019/02/17/implementing-a-regular-expression-engine/
  https://robertheaton.com/2014/02/09/pythons-pass-by-object-reference-as-explained-by-philip-k-dick/
'''

class State:
    global_id = 0
    def __init__(self, is_end: bool = False):
        self.is_end = is_end
        self.transition = {}
        self.epsilon_transition = []

        self.id = State.global_id
        State.global_id += 1

    def __str__(self):
        output = ""
        output += "State {}{}\n".format(self.id, " (END)" if self.is_end else "")
        output += "Transition:\n"
        output += str(["State {}, t={}".format(i.id, t) for t, i in self.transition.items()]) + "\n"
        output += "Epsilon transition:\n"
        output += str(["State {}".format(i.id) for i in self.epsilon_transition]) + "\n"
        return output


class FiniteAutomata:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    def __str__(self):
        def all_transitions(come_from: State) -> [State]:
            output = list(come_from.transition.values())
            output.extend(come_from.epsilon_transition)
            return output

        # Perform depth-first search from given state, print them.
        def traverse_state(stand_on: State) -> str:
            output = ""
            if id(stand_on) in visited_id:
                return output

            output = str(stand_on)
            visited_id.add(id(stand_on))
            
            for t in all_transitions(stand_on):
                output += traverse_state(t)

            return output

        visited_id = set()
        return "Start on state {}\n".format(self.start.id) + traverse_state(self.start)


# Use Thompson's construciton to build a DFA:
# Base rules:
# 1. from --epsilon--> to
# 2. from --a--> to  (single character)
# Inductive rules:
# 1. union
# 2. concatenation
# 3. closure


# Main workhorse function.
def to_NFA(postfix_exp: str) -> FiniteAutomata:
    if postfix_exp == "":
        return from_epsilon()

    stack = []

    for token in postfix_exp:
        if token == "*":
            stack.append(closure(stack.pop()))
        elif token == "|":
            second = stack.pop()
            first = stack.pop()
            stack.append(union(first, second))
        elif token == ".":
            second = stack.pop()
            first = stack.pop()
            stack.append(concat(first, second))
        else:
            stack.append(from_symbol(token))

    assert len(stack) == 1, "Should be only one element left in the stack, but have {}".format(len(stack))

    return stack.pop()


def add_epsilon_transition(come_from: State, to: State) -> None:
    come_from.epsilon_transition.append(to)


def add_transition(come_from: State, to: State, symbol: str) -> None:
    come_from.transition[symbol] = to


# Basic rule 1: From epsilon.
def from_epsilon() -> FiniteAutomata:
    start = State(is_end=False)
    end = State(is_end=True)
    add_epsilon_transition(start, end)
    return FiniteAutomata(start, end)


# Basic rule 2: From a single symbol.
def from_symbol(symbol: str) -> FiniteAutomata:
    start = State(is_end=False)
    end = State(is_end=True)
    add_transition(start, end, symbol)
    return FiniteAutomata(start, end)


# Inductive rules.
def concat(first: FiniteAutomata, second: FiniteAutomata) -> FiniteAutomata:
    add_epsilon_transition(first.end, second.start)
    first.end.is_end = False
    return FiniteAutomata(first.start, second.end)


def union(first: FiniteAutomata, second: FiniteAutomata) -> FiniteAutomata:
    start = State(is_end=False)
    add_epsilon_transition(start, first.start)
    add_epsilon_transition(start, second.start)

    end = State(is_end=True)
    add_epsilon_transition(first.end, end)
    first.end.is_end = False
    add_epsilon_transition(second.end, end)
    second.end.is_end = False

    return FiniteAutomata(start, end)


def closure(nfa: FiniteAutomata) -> FiniteAutomata:
    start = State(is_end=False)
    end = State(is_end=True)
    
    add_epsilon_transition(start, end)
    add_epsilon_transition(start, nfa.start)

    add_epsilon_transition(nfa.end, end)
    add_epsilon_transition(nfa.end, nfa.start)
    nfa.end.is_end = False

    return FiniteAutomata(start, end)

