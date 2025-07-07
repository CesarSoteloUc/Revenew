import subprocess
import shutil
import os

#Ejecutamos el modelo
subprocess.run(["python", "-m", "OPTIMIZADORAPP.run_model_prueba"])

#Definimos los archivos a copiar
archivos_generados = ["Grafico.png", "Cantidad_optima_productos.xlsx"]
#Generamos el archivo lp
archivos_generados += [f for f in os.listdir('.') if f.endswith('.lp')]
#Definimos que los guardaremos en OPTIMIZADORAPP
destino = os.path.join(os.path.dirname(__file__))

#Los movemos y levantamos los procesos
for archivo in archivos_generados:
    if os.path.exists(archivo):
        shutil.move(archivo, os.path.join(destino, archivo))
        print(f"{archivo} movido a {destino}")
    else:
        print(f"{archivo} no encontrado")
