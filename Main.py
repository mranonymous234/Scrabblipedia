import twl
import itertools
from collections import Counter

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def valid_words_from_rack(rack):
    """
    rack: iterable of single-character letters, blank represented as ' ' or '_'
    returns: set of valid uppercase words from TWL06 that can be formed
    """
    rack = [c.upper() for c in rack]
    blanks = rack.count(' ') + rack.count('_')
    fixed_letters = [c for c in rack if c not in (' ', '_')]
    fixed_count = Counter(fixed_letters)

    results = set()

    # maximum word length limited by rack + (optionally) board anchors (here we only form words from rack)
    max_len = len(rack)

    # iterate through possible word lengths (2..max_len because TWL stores words 2..15)
    for L in range(2, max_len+1):
        # generate multisets of letters we might use (choose K letters from fixed letters)
        # Instead of brute-forcing all permutations from dictionary (expensive), use twl.anagram on
        # candidate letter-multisets — but twl.anagram expects a string of letters; we'll generate combos.
        # We'll generate combinations with replacement for blanks by substituting letters.
        # Strategy: for each choice of how many blanks to use (b), replace them by all letter combos.
        for b in range(0, min(blanks, L)+1):
            k = L - b  # how many non-blank letters to select from fixed_letters
            if k > len(fixed_letters):
                continue
            # generate all unique combinations (multiset) of size k from fixed_letters
            # we'll generate permutations via combinations of indices to avoid combinatorial explosion for small racks
            # simple approach: generate all permutations of all subsets of fixed_letters of size k
            for subset in set(itertools.permutations(fixed_letters, k)):
                base = ''.join(subset)
                if b == 0:
                    # no blanks: check anagrams directly
                    for w in twl.anagram(base):
                        if len(w) == L:
                            results.add(w.upper())
                else:
                    # b blanks: substitute blanks with all possible letter tuples of length b
                    # for 1-2 blanks this is fine; for >2 blanks this becomes expensive
                    for replacement in itertools.product(ALPHABET, repeat=b):
                        candidate = base + ''.join(replacement)
                        for w in twl.anagram(candidate):
                            if len(w) == L:
                                results.add(w.upper())

    return results

# Example usage:
rack1 = ['A','N','C',' ','L','F','T']   # blank as ' '
words = valid_words_from_rack(rack1)
print(sorted(list(words))[:50])
print("Total:", len(words))
