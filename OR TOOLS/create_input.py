#Generamos los Inputs del Excel con los cuales trabajaremos.

import pandas as pd
from classes import *

def create_input(path):
    input_set = InputSet()
    input_set.products = carga_productos(path)
    input_set.machine = cargar_machine(path)
    return input_set

def carga_productos(path):
    list_productos = []
    df_productos = pd.read_json(f'{path}optimization_problem_data.json')

    product_a = Product(
        _id='A',
        price=df_productos['Price_Product_A'][0],
        production_time={
            'Machine_1': df_productos['Product_A_Production_Time_Machine_1'][0],
            'Machine_2': df_productos['Product_A_Production_Time_Machine_2'][0]
        }
    )
    list_productos.append(product_a)

    product_b = Product(
        _id='B',
        price=df_productos['Price_Product_B'][0],
        production_time={
            'Machine_1': df_productos['Product_B_Production_Time_Machine_1'][0],
            'Machine_2': df_productos['Product_B_Production_Time_Machine_2'][0]
        }
    )
    list_productos.append(product_b)

    return list_productos

def cargar_machine(path):
    list_machines = []
    df = pd.read_json(f'{path}optimization_problem_data.json')
    machine1 = Machine(
        _id='Machine_1',
        available_hours=df['Machine_1_Available_Hours'][0]
    )
    list_machines.append(machine1)

    machine2 = Machine(
        _id='Machine_2',
        available_hours=df['Machine_2_Available_Hours'][0]
    )
    list_machines.append(machine2)

    return list_machines
