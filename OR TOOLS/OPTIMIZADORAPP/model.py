from ortools.linear_solver import pywraplp
from .constraints import *
from .classes import InputSet
import random

class ModelClass:
    def __init__(self, input_set: InputSet):
        self.solver = pywraplp.Solver.CreateSolver("SCIP") #Selección del solver
        self.objective_function = None
        self.inputs = input_set
        self.outputs = {}
        self.x = {}

        # Ejecutar funciones de construcción del modelo
        self.create_variables()
        self.add_constraints()
        self.add_objective()


    def create_variables(self):
        solver = self.solver

        # X_a, X_b
        for product in self.inputs.products:
                self.x[product.id] = solver.IntVar(0, solver.infinity(), f"x_{product.id}")

    def add_constraints(self):
        solver = self.solver
        time_machine(self.inputs, self, solver)

    def add_objective(self):
        solver = self.solver
        objective = solver.Sum(
            product.price * self.x[product.id]
            for product in self.inputs.products
        )
        self.objective_function = objective
        solver.Maximize(objective)

    def export_model(self):
        lp_model_str = self.solver.ExportModelAsLpFormat(False)
        random_number = random.randint(1, 100)
        filename = f'modelo_{random_number}.lp'
        with open(filename, 'w') as f:
            f.write(lp_model_str)
        print(f"Modelo exportado como {filename}")
