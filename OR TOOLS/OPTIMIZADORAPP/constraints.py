from .classes import InputSet
#Generamos las restricciones
def time_machine(input_set: InputSet, m_class, solver):
    for machine in input_set.machine:
        constrain = 0
        for product in input_set.products:
            constrain += product.production_time[machine.id]*m_class.x[product.id]
        solver.Add(constrain <= machine.available_hours)
