# Wordle_Solver
### A program to solve the daily wordle
The algorithm can correctly solve each possible word within the required 6 guesses!!

It looks at the most common letters to determine a good guess. In some cases this method fails us. When there are multiple options availible with the same commonality score, and there is a small number of valid guesses, the algorithm will pick a incorrect word that uses the least common letters to help eliminate options from these best guesses.

For example, the valid words remaining are [fight', 'light', 'might', 'night', 'wight']. Picking any of these words only removes 1 option, but if we can guess a word using 4 or 5 of the unique letters in this list of words, we can know for certain which word is the correct answer.

#### Project is currently a work in progress.
The goal is to have both a playable game where it will randomly generate a word for you to guess, and a mode where it will solve the wordle of the day

### Project structure
The WordleLibrary folder contains the core algorithms and coding logic. The WordleSolver folder contains the beeware frontend for the app. 
Currently working to integrate the beeware frontend with the existing code
Currently set Beeware integration as my default branch so it shows up in my github activity. Once ready to pull it across to main will switch default branches again.
