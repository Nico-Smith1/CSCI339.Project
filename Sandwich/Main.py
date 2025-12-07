from collections import defaultdict
from itertools import product

########################################
#                TAPE
########################################
class Tape:
    def __init__(self, input_string="", blank="#"):
        self.tape = defaultdict(lambda: blank)
        for i, ch in enumerate(input_string):
            self.tape[i] = ch
        self.blank = blank
        self.head = 0

    def read(self):
        return self.tape[self.head]

    def write(self, ch):
        self.tape[self.head] = ch

    def move(self, direction):
        if direction == "R":
            self.head += 1
        elif direction == "L":
            self.head -= 1
        else:
            raise ValueError("direction must be 'L' or 'R'")

    def __str__(self):
        indices = list(self.tape.keys()) + [self.head]
        lo, hi = min(indices), max(indices)
        s = []
        for i in range(lo, hi + 1):
            ch = self.tape[i]
            if i == self.head:
                s.append(f"[{ch}]")
            else:
                s.append(f" {ch} ")
        return "".join(s)


########################################
#         TURING MACHINE CLASS
########################################
class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet,
                 transitions, start_state, accept_states, blank="#"):

        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.blank = blank

    def run(self, input_string, max_steps=5000, verbose=False):
        """
        Executes the TM and RETURNS ALL TRANSITION LOGS
        so the GUI can display them.
        """
        tape = Tape(input_string + self.blank, blank=self.blank)
        state = self.start_state
        step = 0

        transitions_log = []   # <--- THIS FIXES THE GUI ERROR

        def log(msg):
            transitions_log.append(msg)
            if verbose:
                print(msg)

        log(f"START: {state} {tape}")

        while step < max_steps:

            # Accept if in accept state AND reading blank
            if state in self.accept_states and tape.read() == self.blank:
                log(f"ACCEPTED in state {state}")
                break

            symbol = tape.read()
            key = (state, symbol)

            # No transition → halt
            if key not in self.transitions:
                log(f"HALT (no transition): {key}")
                break

            new_state, write, move = self.transitions[key]
            tape.write(write)
            tape.move(move)
            state = new_state
            step += 1

            log(f"step {step}: {state} {tape}")

        return {
            "final_state": state,
            "accepted": (state in self.accept_states and tape.read() == self.blank),
            "steps": step,
            "tape": tape,
            "transitions": transitions_log   # <--- GUI USES THIS
        }


########################################
#     BUILD SANDWICH TM (COUNT CHECKER)
########################################
def build_sandwich_tm(rules):
    """
    rules: dict like {"A":2, "C":1, "D":0, ...}
    Only symbols with >0 counts are allowed on the tape.
    """
    ingredients = [ing for ing, need in rules.items() if need > 0]
    needs = [rules[ing] for ing in ingredients]

    forbidden = {ing for ing, need in rules.items() if need == 0}

    # helper: encode state from counts
    def encode(counts):
        if not ingredients:
            return "q_0"
        return "q_" + "_".join(f"{ing}{c}" for ing, c in zip(ingredients, counts))

    states = set()
    transitions = {}

    # Generate all possible counting states
    if ingredients:
        for counts in product(*[range(n + 1) for n in needs]):
            states.add(encode(counts))
    else:
        states.add("q_0")

    reject_state = "q_reject"
    states.add(reject_state)

    accept_state = encode(tuple(needs))
    accept_states = {accept_state}

    start_state = encode(tuple(0 for _ in ingredients))

    allowed_symbols = set(rules.keys())

    # Build transitions
    if ingredients:
        for counts in product(*[range(n + 1) for n in needs]):
            state = encode(counts)

            for sym in allowed_symbols:

                # Forbidden → reject
                if sym in forbidden:
                    transitions[(state, sym)] = (reject_state, sym, "R")
                    continue

                idx = ingredients.index(sym)
                current = counts[idx]
                maxc = needs[idx]

                # Too many of symbol → reject
                if current == maxc:
                    transitions[(state, sym)] = (reject_state, sym, "R")
                else:
                    new_counts = list(counts)
                    new_counts[idx] += 1
                    new_state = encode(tuple(new_counts))
                    transitions[(state, sym)] = (new_state, sym, "R")

    else:
        # No ingredients allowed → any letter rejects
        for sym in allowed_symbols:
            transitions[(start_state, sym)] = (reject_state, sym, "R")

    return TuringMachine(
        states=states,
        input_alphabet=allowed_symbols,
        tape_alphabet=allowed_symbols | {"#"},
        transitions=transitions,
        start_state=start_state,
        accept_states=accept_states,
        blank="#"
    )


########################################
#             OPTIONAL DEMO
########################################
if __name__ == "__main__":
    rules = {"A": 2, "B": 1, "C": 0}
    tm = build_sandwich_tm(rules)

    test = "AAB"
    print("\nTesting:", test)
    result = tm.run(test, verbose=True)
    print("Accepted?", result["accepted"])
