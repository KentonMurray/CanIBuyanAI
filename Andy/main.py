"""
Wrapper for latest version of wof_solver
As of 12/3/25, uses wof_solver3

"""

from wof_solver3 import wof_solver
"""
main function

def wof_solver(pattern, attempted_letters=None,
               words_path="data/words.txt",
               phrases_path="data/phrases.txt"):
    Returns dict:
        {
            "solutions": [string, string, string],
            "ranked": [string#1, string#2, string#3],
            "next_letter": [(letter1, count), (letter2, count)]
        }
"""

__all__ = ['wof_solver']