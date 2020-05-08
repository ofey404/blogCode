'''
@Author: Ofey Chan
@Date: 2020-05-08 20:28:15
@LastEditors: Ofey Chan
@LastEditTime: 2020-05-08 22:50:24
@Description: Nondeterministic finite automata matcher. The main workhorse file.
@Reference: 
'''

from parser import parse_regex_to_postfix
from NFA import to_NFA, FiniteAutomata, State
from typing import Callable  # for lambda type hint


# Workhorse function.
# Create a matcher function which return match or not from given regex.
def create_matcher(regex: str = "") -> Callable[[FiniteAutomata, str], bool]:
    postfix_exp = parse_regex_to_postfix(regex)
    nfa = to_NFA(postfix_exp)

    return lambda word: search(nfa, word)


# Follow the automata step by step.
def search(nfa: FiniteAutomata, word: str) -> bool:
    current_states = []
    current_states.extend(all_next_states_from(nfa.start))

    for character in word:
        next_states = []

        for state in current_states:
            if character not in state.transition:
                continue
            next = state.transition[character]
            next_states.extend(all_next_states_from(next))

        current_states = next_states

    # Check after len(word) step, whether there are any end state.
    has_end_state = False
    for final_state in current_states:
        if final_state.is_end:
            has_end_state = True
            break
    return has_end_state
    

# Return the list of given state and all possible states can be reach by any
# epsilon transition chain from given state.
# Visited 
def all_next_states_from(state: State) -> [State]:
    visited = set()
    output = []
    if len(state.epsilon_transition) > 0:
        for st in state.epsilon_transition:
            if st not in visited:
                visited.add(st)
                output.extend(all_next_states_from(st))
    else:  # DEBUG: If this `else` should be deleted?
        output.append(state)
    return output