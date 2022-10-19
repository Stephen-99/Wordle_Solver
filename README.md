# Wordle_Solver
A program to solve the daily wordle
It looks at the most common letters to determine a good guess. In some cases this method fails us. When there are multiple options availible with the same commonality score, and there is a small number of valid guesses, the algorithm will pick a incorrect word that uses the least common letters to help eliminate options from these bet guesses.
For example, the valid words remaining are [fight', 'light', 'might', 'night', 'wight']. Picking any of these words only removes 1 option, but if we can guess a word using 4 or 5 of the unique letters in this word, we can know for certain which word is the correct answer.

Currently a work in progress.
The goal is to have both a playable game where it will randomly generate a word for you to guess, and a mode where it will solve the wordle of the day
