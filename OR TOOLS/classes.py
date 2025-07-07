#Se crean as clases correspondientes
class InputSet:
    def __init__(self):
        # Conjuntos
        self.products = [] 
        self.machine = []

class Product:
    def __init__(self, _id, price, production_time):
        self.id = _id
        self.price = price
        self.production_time = production_time

    def __repr__(self):
        return f"Product(ID: {self.id}, Precio: {self.price}, Tiempo de demora de producción: {self.production_time})"


class Machine:
    def __init__(self, _id,available_hours):
        self.id = _id
        self.available_hours = available_hours

    def __repr__(self):
        return f"Machine,(Maquína: {self.id}, Horas Disponible: {self.available_hours})"
