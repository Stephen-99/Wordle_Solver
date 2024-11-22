# Wordle_Solver
## What it is
An app that solves the wordle for you!
It provides you with the best next guess to take.
It also has an option to play wordle within the app

## How to use it
### Windows install instructions
1. Download the .msi file
2. Double click the msi to install
3. Search for "Wordle Solver" in windows search to run the program

### Windows uninstall
1. Search for "add or remove programs" in windows search
2. Locate Wordle Solver, slect the "..." and  select uninstall

### Android
Download on the google play store (COMING SOON)
   
## How the solver works
The algorithm can correctly solve each possible word within the required 6 guesses!!
It looks at the most common letters to determine a good guess. In some cases this method fails us. When there are multiple options availible with the same commonality score, and there is a small number of valid guesses, the algorithm will pick a incorrect word that uses the least common letters to help eliminate options from these best guesses.
For example, the valid words remaining are [fight', 'light', 'might', 'night', 'wight']. Picking any of these words only removes 1 option, but if we can guess a word using 4 or 5 of the unique letters in this list of words, we can know for certain which word is the correct answer.

## Project structure
The WordleLibrary folder contains the core algorithms and coding logic. The WordleSolver folder contains the beeware frontend for the app. 

## Support Me
Enjoyed using the app or found my code useful?
Please consider supporting me for my work:
https://buymeacoffee.com/stephen99

