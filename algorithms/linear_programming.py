#co = coefficients

class Simplex:
    def __init__(self, constraints_co, constraint_vals, objective_co, var_names = None, is_maximising = True):
        self.num_of_constraints = len(constraints_co)
        self.num_of_vars = len(constraints_co[0])
        self.isMaximising = is_maximising
        self.basic_vars = []
        self.steps = []
        self.tableau = self.create_tableau(constraints_co, constraint_vals, objective_co)

        self.record_step(
            "The table has been created."
        )

        for i in range(self.num_of_constraints):
            self.basic_vars.append(self.num_of_vars + i)

        self.var_names = var_names or ['x', 'y', 'z']
        print("This is the initial Tableau")
        self.print_tableau()

    def record_step(self, explanation, pivot_col=None, pivot_row= None, pivot_val=None):
        self.steps.append({
            "headers": self.get_headers(),
            "basic_vars": [self.current_var(i) for i in self.basic_vars] + ["P"],
            "tableau" : [row[:] for row in self.tableau],
            "pivot_col": pivot_col,
            "pivot_row": pivot_row,
            "explanation": explanation,
            "pivot_val": pivot_val
        })

    def explain_pivot_operation(self, row, col):
        var = self.current_var(col)
        return f"{var} is now the basic variable in row {row+1}."

    def create_tableau(self, constraints_co, constraint_vals, objective_co):
        tableau = []
        for i in range(self.num_of_constraints):
            tableau.append(constraints_co[i] + [0] * self.num_of_constraints + [constraint_vals[i]])
            tableau[i][self.num_of_vars] = 1
        if self.isMaximising:
            for i in range(len(objective_co)):
                objective_co[i] = -objective_co[i]
        tableau.append(objective_co + [0] * self.num_of_constraints + [0])
        
        return tableau

    def explain_pivot_column(self, col):
        var = self.current_var(col)
        value = self.tableau[-1][col]

        return (
            f"The most negative value in the objective row is {value:.2f} in column {var}. So the pivot column is {var}."
        )
    
    def explain_pivot_row(self, row, ratios):
        ratio_text = ", ".join([f"{r[0]:.2f}" for r in ratios])
        return (
            f"Using the ratio test ({ratio_text}), the smallest positive ratio "
            f"is in row {row+1}, so this is the pivot row."
        )



    def pivot(self, row, col):
        pivot_value = self.tableau[row][col]

        for i in range(len(self.tableau[row])):
            self.tableau[row][i] = self.tableau[row][i]/pivot_value
        
        self.record_step(f"Divide row {row+1} by pivot value {pivot_value:.2f}.")

        for this_row in range(len(self.tableau)):
            if this_row != row:
                factor = self.tableau[this_row][col]
                for this_col in range(len(self.tableau[this_row])):
                    self.tableau[this_row][this_col] -= factor * self.tableau[row][this_col]
    def get_pivot_col(self):
        min_value = min(self.tableau[-1][:-1])
        if min_value >= 0:
            return None
        return self.tableau[-1][:-1].index(min_value)

    def get_pivot_row(self, col):
        ratios = [
            (self.tableau[i][-1] / self.tableau[i][col], i)
            for i in range(self.num_of_constraints)
            if self.tableau[i][col] > 0
        ]

        if not ratios:
            return None, []

        row = min(ratios)[1]
        return row, ratios

    def extract_solution(self):
        all_vars = [0] * (self.num_of_vars + self.num_of_constraints)
        for i in range(len(self.basic_vars)):
            var_index = self.basic_vars[i]
            all_vars[var_index] = self.tableau[i][-1]


        original_vars = all_vars[:self.num_of_vars]
        slack_vars = all_vars[self.num_of_vars:]

        p_value = self.tableau[-1][-1]
        return original_vars, slack_vars, p_value

    def current_var(self, index):
        if index < self.num_of_vars:
            return self.var_names[index]
        else:
            return f"s{index-self.num_of_vars+1}"

    def get_headers(self):
        headers = ["Basic Variable"]
        for i in range(self.num_of_constraints + self.num_of_vars):
            headers.append(self.current_var(i))
        headers.append("Values")

        return headers

    def solve(self):
        while True:
            pivot_col = self.get_pivot_col()

            if pivot_col is None:
                self.record_step("All values in the objective row are non-negative. So, the optimal solution has been found.",)
                break

            col_explain = self.explain_pivot_column(pivot_col)

            pivot_row, ratios = self.get_pivot_row(pivot_col)

            if pivot_row is None:
                self.record_step("No feasible solution exists.", pivot_col = pivot_col)
                return None

            row_explain = self.explain_pivot_row(pivot_row, ratios)
            self.record_step(col_explain + " " + row_explain, pivot_col, pivot_row)

            self.pivot(pivot_row, pivot_col)
            self.basic_vars[pivot_row] = pivot_col

            self.record_step(self.explain_pivot_operation(pivot_row, pivot_col), pivot_col=pivot_col, pivot_row= pivot_row)

        return self.extract_solution()

A = [
    [2, 3, 0],
    [1, 2, 5],
    [0, 5, 3]
]
b = [10, 60, 40]
c = [8, 5, 7]
variables = ['x', 'y', 'z']

solver = Simplex(A, b, c, variables)
n_vars, s_vars, sol = solver.solve()

for item in range(len(n_vars)):
    print(f"{variables[item]} = {n_vars[item]}")

for item in range(len(s_vars)):
    print(f"s{item+1} = {s_vars[item]}")

if solver.isMaximising:
    print(f"When P is maximised = {sol}")
else:
    print(f"When P is minimised = {sol}")