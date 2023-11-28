# [CS50AI Week 3, Optimization](https://cs50.harvard.edu/ai/2023/weeks/3/) - [Crossword](https://cs50.harvard.edu/ai/2023/projects/3/crossword/)

An AI that solves a crossword puzzle by representing it as a Constraint Satisfaction Problem (CSP). 

## Summary
We can model the problem of solving crossword puzzles as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence). 


As with many constraint satisfaction problems, these variables have both unary and binary constraints. The unary constraint on a variable is given by its length. For Variable 1, for instance, the value BYTE would satisfy the unary constraint, but the value BIT would not (it has the wrong number of letters). Any values that don’t satisfy a variable’s unary constraints can therefore be removed from the variable’s domain immediately.


The binary constraints on a variable are given by its overlap with neighboring variables. Variable 1 has a single neighbor: Variable 2. Variable 2 has two neighbors: Variable 1 and Variable 3. For each pair of neighboring variables, those variables share an overlap: a single square that is common to them both. We can represent that overlap as the character index in each variable’s word that must be the same character.


The challenge ahead, then, is to write a program to find a satisfying assignment: a different word (from a given vocabulary list) for each variable such that all of the unary and binary constraints are met.


## Links
[CS50AI Week 3](https://cs50.harvard.edu/ai/2023/weeks/3/)

[CS50AI Week 3 Notes](https://cs50.harvard.edu/ai/2023/notes/3/)

[CS50AI Week 3 Projects](https://cs50.harvard.edu/ai/2023/projects/3/)

[CS50AI Week 3 Projects - Crossword](https://cs50.harvard.edu/ai/2023/projects/3/crossword/)


