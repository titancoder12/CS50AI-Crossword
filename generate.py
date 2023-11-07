import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Loop over nodes
        domains = (self.domains).copy()
        for domain in domains:

            # Loop over domain of nodes
            possibilities = domains[domain].copy()
            for possibility in possibilities:
                
                # Remove node given condition
                if domain.length != len(possibility):
                    #print(possibility)
                    self.domains[domain].remove(possibility)
            #print(f"ENFORCED: {self.domains}")


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        """self.enforce_node_consistency()
        revised = False
        domains_x = (self.domains[x]).copy()
        for domain_x in domains_x:

            domains_y = (self.domains[y]).copy()
            satisfied = True

            for domain_y in domains_y:
                if len(domain_y) != len(domain_x):
                    satisfied = False
                test = {x: domain_x, y: domain_y}
                if not self.consistent(test):
                    satisfied = False
            
            if satisfied == False:
                self.domains[x].remove(domain_x)
                revised = True
        print(f"REVISED: {self.domains}")
        if revised == True:
            return True
        else:
            return False"""
        #print(f"REVISED: {self.domains}")
        revised = False
        x_domains = self.domains[x].copy()
        y_domains = self.domains[y].copy()
        for x_domain in x_domains:
            not_satisfied = 0
            for y_domain in y_domains:
                overlap = self.crossword.overlaps[x, y]
                if len(y_domain) != len(x_domain):
                    not_satisfied += 1
                elif overlap:
                    a, b = overlap
                    if x_domain[a] != y_domain[b]:
                        not_satisfied += 1
            if not_satisfied == len(y_domains):
                self.domains[x].remove(x_domain)
                revised = True
                break
        return revised


                
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        self.enforce_node_consistency()
        # TODO
        if arcs == None:
            arcs_c = list(self.crossword.overlaps.keys())
        else:
            arcs_c = arcs.copy()
        #print(arcs_c)
        while len(arcs_c) != 0:
            (X, Y) = arcs_c.pop()
            if self.revise(X, Y):
                if self.domains[X] == 0:
                    return False
                for Z in self.crossword.neighbors(X):
                    if Z != Y:
                        arcs_c.append((Z, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #print("keys:")
        #print(type(assignment))
        """if len(assignment) != 0:
            for key in assignment:
                #print(key)
                if key is None:
                    return False
                
        else:
            return False
        return True"""
        for variable in self.crossword.variables:
            #print(variable)
            #print(assignment)
            if variable in assignment:
                if assignment[variable] is None:
                    return False
            if variable not in assignment:
                return False
        return True
        
        #return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = list(assignment.values())
        values_s = set(values)

        # Check if any duplicates
        if len(values) != len(values_s):
            return False
        
        keys = list(assignment.keys())
        for i in range(len(keys)):
            if keys[i] is None:
                return False
            if keys[i].length != len(assignment[keys[i]]):
                return False
            for j in range(len(keys)):
                if keys[i] != keys[j]:
                    if self.crossword.overlaps[keys[i], keys[j]] is not None:
                        (x, y) = self.crossword.overlaps[keys[i], keys[j]]
                        if assignment[keys[i]][x] != assignment[keys[j]][y]:
                            return False
            
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # \/ TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO \/
        """values = []
        for domain in self.domains[var]:
            eliminations = 0
            
            for neighbor in self.crossword.neighbors(var):
                for n_domain in self.domains[neighbor]:
                    if neighbor not in list(assignment.keys()):
                        test = {var: domain, neighbor: n_domain}
                        if not self.consistent(test):
                            eliminations += 1
            values.append({"domain" :domain, "eliminations":eliminations})
        x = lambda e: e["eliminations"]
        values.sort(key=x)
        print(values)
        return_val = []
        for value in values:
            return_val.append(value["domain"])
        return return_val"""
        return self.domains[var]
        
        # /\ TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO /\

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # \/ TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO \/
        for key in list(self.domains.keys()):
            if key not in assignment:
                return key
        # /\ TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO /\

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # TODO
        if self.assignment_complete(assignment):
            print("return Assignment")
            return assignment

        assignment_c = assignment.copy()

        var = self.select_unassigned_variable(assignment_c)
        i = 1
        #print(f"variable {var} has domains: {self.domains}")
        for value in self.order_domain_values(var, assignment):
            if i == 200:
                break
            #print(f"Iteration {i}/{len(self.domains[var])}")
            #print(value)
            test = assignment_c.copy()
            test[var] = value
            if (len(value) == var.length) and self.consistent(test):
                assignment_c[var] = value
                result = self.backtrack(assignment_c)
                #print(result)
                #if result != None:
                if result != None:
                    #print("return REsult")
                    return result
                #print("pop!")
                assignment_c.pop(var)
                i+=1
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
