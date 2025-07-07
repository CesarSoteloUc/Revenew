from model import *
import time
from read_excel import *
from create_input import create_input
from ortools.linear_solver import pywraplp
from output import export
from grafico import plot_multiple_solutions

def main():
    inicio = time.time()
    excel_path = 'optimization_problem_data.csv'
    path = 'tmp/'
    expected_cols = [
    'Product_A_Production_Time_Machine_1',
    'Product_A_Production_Time_Machine_2',
    'Product_B_Production_Time_Machine_1',
    'Product_B_Production_Time_Machine_2',
    'Machine_1_Available_Hours',
    'Machine_2_Available_Hours',
    'Price_Product_A',
    'Price_Product_B'
]

    loader = DataLoader(expected_columns=expected_cols)
    try:
        df = loader.leer_excel(excel_path, path)
    except Exception as e:
        print(f"Error cargando y validando datos: {e}")
        return

    input_set = create_input(path)
    print("==== Productos cargados ====")
    for producto in input_set.products:
        print(producto)
    print("\n==== Máquinas cargadas ====")
    for machine in input_set.machine:
        print(machine)

    print(round(time.time() - inicio))
    modelo = ModelClass(input_set)
    solver = modelo.solver
    print(round(time.time() - inicio))
    status = solver.Solve()
    print(round(time.time() - inicio))

    if status == pywraplp.Solver.OPTIMAL:
        print(f"Se encontro solucion optima")
        print(f"Valor: {solver.Objective().Value():,.2f}")
        modelo.export_model()
        export(modelo)
    elif status == pywraplp.Solver.FEASIBLE:
        print(f"Se encontro solucion no optima")
        print(f"Valor: {solver.Objective().Value():,.2f}")

    else:
        print("Solucion infactible")
    #Desde aca generamos distintos valores para plotear los valores de la funcion objetivo
    solutions = []
    max_a = 10
    max_b = 10
    for a in range(max_a+1):
        for b in range(max_b+1):
            modelo = ModelClass(input_set)
            solver = modelo.solver
            modelo.x['A'].SetBounds(a, a)
            modelo.x['B'].SetBounds(b, b)

            status = solver.Solve()
            if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
                obj_val = solver.Objective().Value()
                solutions.append( (a, b, obj_val) )
                print(f"Sol factible encontrada: A={a}, B={b}, Obj={obj_val:.2f}")
    plot_multiple_solutions(solutions)
    print("END")
if __name__ == "__main__":
    main()