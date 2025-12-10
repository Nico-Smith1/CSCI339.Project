import random
from nltk import CFG
from nltk.parse import ChartParser
from collections import Counter

from Main import build_sandwich_tm

# Grammar to generate "sandwiches"
grammar = CFG.fromstring('''
S -> P P P | P P P P | P P P P P | P P P P P P| P P P P P P P | P P P P P P P P
P -> "A" | "C" | "T" | "D" | "E" | "F" | "G" | "H" | "I" | "J"

'''

                         )

parser = ChartParser(grammar)


def test_sandwich(s):
    try:
        parses = list(parser.parse(list(s)))
        return len(parses) > 0
    except ValueError:
        return False


def generate_order(grammar):
    """Randomly generate a sandwich string from CFG."""
    def expand(symbol):
        # Terminal symbols
        if symbol in grammar._lexical_index:
            return [symbol]

        production = random.choice(grammar.productions(lhs=symbol))
        result = []

        for sym in production.rhs():
            # Terminal case
            if isinstance(sym, str) and sym.startswith("'") and sym.endswith("'"):
                result.append(sym[1:-1])
            else:
                result.extend(expand(sym))
        return result

    return ''.join(expand(grammar.start()))


def count_ingredients(sandwich):
    """Return dict of ingredient counts A–J."""
    counts = Counter(sandwich)
    return {
        "A": counts.get("A", 0),
        "T": counts.get("T", 0),
        "C": counts.get("C", 0),
        "D": counts.get("D", 0),
        "E": counts.get("E", 0),
        "F": counts.get("F", 0),
        "G": counts.get("G", 0),
        "H": counts.get("H", 0),
        "I": counts.get("I", 0),
        "J": counts.get("J", 0),
    }


if __name__ == "__main__":
    # Optional debug/demo
    sandwich = generate_order(grammar)
    print("Generated:", sandwich)
    print("Counts:", count_ingredients(sandwich))
    tm = build_sandwich_tm(count_ingredients(sandwich))
