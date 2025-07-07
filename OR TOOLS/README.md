# Proyecto de Optimización Revenew

Este documento explica paso a paso la realización del proyecto, detallando su desarrollo, diseño de clases, estructura de carpetas y generación de gráficos.

## 1. Descarga y creación de carpeta

En primera instancia, se descargaron los archivos Excel y se creó la carpeta principal del proyecto llamada **Revenew** para mantener la organización.

## 2. Creación del modelo

### 2.1. Lectura y validación de datos - `read_excel.py`

Se creó el archivo `read_excel.py`, cuyo objetivo es:

- Leer archivos en formato CSV o Excel (.xls/.xlsx).
- Convertirlos en un DataFrame y exportarlos a formato JSON para su uso en el modelo.
- Validar los datos cargados, verificando:
  - La existencia de columnas requeridas.
  - Que no haya valores nulos.
  - La unicidad de los identificadores de productos (evitando duplicados).
  - Que los tipos de datos correspondan a lo esperado en cada columna.

En caso de incumplir estas validaciones, la función levanta un error y detiene la ejecución, asegurando la calidad de los datos ingresados al modelo.

**DataLoader:** Este módulo cumple la función de un DataLoader, asegurando la correcta carga y validación de los datos antes de su procesamiento.

### 2.2. Definición de clases - `classes.py`

Define:

- **Producto:** atributos como `production_time` (tiempo de producción en cada máquina) y `price`.
- **Machine:** información de cada máquina disponible.
- **InputSet:** agrupa los conjuntos de productos y máquinas para ser usados como input en el modelo.

**Diseño:** El atributo `production_time` está en Producto y no en Machine, ya que cada producto tiene tiempos de producción distintos en cada máquina. La máquina se considera como un recurso habilitante (una "compuerta"). Esto reduce iteraciones y mantiene un código más limpio y eficiente.

### 2.3. Generación de inputs - `create_input.py`

Define funciones para crear inputs del modelo:

- `cargar_productos`: genera objetos Producto leyendo el JSON, diferenciando entre productos A y B según su nombre y asignando atributos manualmente (debido a la estructura del Excel).
- `cargar_machine`: genera objetos Machine.
- `create_input`: integra ambas funciones y devuelve el input completo para el modelo.

**Nota:** Se prefirió no modificar el archivo Excel original y realizar la asignación manual de atributos. Con una estructura distinta se podría automatizar vía indexación.

### 2.4. Definición de restricciones - `constraints.py`

Contiene la función `time_machine`, la cual genera las restricciones de tiempo de máquina:

> Suma de [product.production_time * cantidad_producida] menor o igual a horas_disponibles

Se añaden al modelo mediante `solver.Add()` de OR-Tools.

### 2.5. Creación del modelo de optimización - `model.py`

Define la clase **ModelClass**, que incluye:

- `create_variables`: crea las variables de decisión como enteras mayores o iguales a 0.
- `add_constraints`: añade las restricciones generadas en `constraints.py`.
- `add_objective`: define la función objetivo de maximización.
- `export_model`: exporta el modelo en formato `.lp` para revisión.

**Solver utilizado:** SCIP, eficiente en problemas de programación entera y mixta.

### 2.6. Exportación de resultados - `output.py`

Genera un archivo Excel llamado **Cantidad_optima_productos.xlsx**, mostrando los resultados óptimos obtenidos. Además se genera un archivo `.lp` en el cual podemos ver cómo está construido el modelo, sus restricciones, variables y función objetivo (El lp se genera en rund_model_prueba.py).

### 2.7. Ejecución del modelo - `run_model_prueba.py`

Este script:

- Integra todas las funciones y clases.
- Imprime en consola si la solución es óptima, factible o infactible.
- Muestra los tiempos de ejecución en cada etapa, permitiendo analizar el rendimiento y eficiencia del pipeline.

### 2.8. Generación de gráficos - `grafico.py`

Se creó el módulo `grafico.py` para:

- Generar gráficos de barras comparando diferentes soluciones factibles con su valor en la función objetivo.
- Mostrar en el eje X la combinación de cantidades (por ejemplo, A=2, B=4) y en el eje Y el valor correspondiente en la función objetivo.
- Guardar automáticamente el gráfico generado como **Grafico.png** en el proyecto.

**Importante:** el gráfico solo considera soluciones factibles según las restricciones del modelo.

---

## Resumen de imports por archivo

### `model.py`
- **Internos:** `from classes import InputSet`, `from constraints import *`, `from create_input import create_input`
- **Externos:** `from ortools.linear_solver import pywraplp`, `import random`

### `create_input.py`
- **Internos:** `from classes import Producto, Machine, InputSet`
- **Externos:** `import pandas as pd`

### `constraints.py`
- **Internos:** `from classes import InputSet`
- **Externos:** Ninguno

### `run_model_prueba.py`
- **Internos:** `from model import *`, `from read_excel import *`, `from create_input import create_input`, `from output import export`, `from grafico import plot_multiple_solutions`
- **Externos:** `import time`, `from ortools.linear_solver import pywraplp`

### `output.py`
- **Internos:** `from model import *`
- **Externos:** `from openpyxl import Workbook`

### `read_excel.py`
- **Internos:** Ninguno
- **Externos:** `import pandas as pd`

### `classes.py`
- **Internos:** Ninguno
- **Externos:** Ninguno

### `grafico.py`
- **Internos:** Ninguno
- **Externos:** `import matplotlib.pyplot as plt`

---

## 3. Generación del entorno virtual

### 3.1. Creación del archivo `requirements.txt`

Se creó un archivo `requirements.txt` con todas las librerías requeridas para el uso del código:

- django
- pandas
- numpy
- ortools
- matplotlib
- openpyxl

### 3.2. Creación del entorno virtual

Para crear el entorno virtual en VS Code, sigue estos pasos:

1. Selecciona **"Create Virtual Environment"**.
2. Elige **venv** como tipo de entorno.
3. Selecciona la versión de Python que vas a utilizar (por ejemplo, Python 3.10). Si no la tienes instalada, debes hacerlo antes de este paso.
4. Selecciona el archivo `requirements.txt` para instalar las dependencias.

Una vez creada la carpeta **.venv**, abre la terminal dentro de la carpeta del proyecto y ejecuta:

pip install -r `requirements.txt`

Finalmente, ejecuta el código para verificar que todo funcione correctamente (dentro del entorno virtual creado).

NOTA: Debes activar el entorno virtual ejecutando venv\Scripts\activate. Una vez activado, instala las dependencias con el comando pip install -r `requirements.txt` para asegurarte de que se instalen solo en el entorno virtual y no globalmente. Verifica que todas las librerías requeridas estén instaladas usando pip list. También confirma que el código se ejecute dentro del entorno virtual y no de manera global. Hay mas formas de y orden de crear el entorno virtual usa la qye mas te acomode.


# Importante.
Hasta este punto, he aplicado mi conocimiento de forma independiente. Sin embargo, después del último paso comencé a tener complicaciones, principalmente por mi falta de experiencia con Django. Para entenderlo más rápido y completar el proceso, utilicé ayuda de IA, vi tutoriales en YouTube y consulté información en la web.

## 3. Implementación Django.

### 3.1. Creación del Proyecto.

Dentro del entono virtual ejecutamos el comando:
django-admin startproject `Nombre del proyecto` .

En nuestro caso `Nombre del proyecto` = `OPTIMIZADOR`.

### 3.1. Creación de la APP.

Ejecutamos python manage.py startapp `OPTIMIZADORAPP` para generar una APP dentro de nuestro proyecto, esto se debe hacer en el entorno virtual de nuestra carpeta.
En nuestro caso (.venv) PS C:\Users\Asus\Desktop\Revenew\OR TOOLS> python manage.py startapp OPTIMIZADORAPP. Como vimos anteriormente el código esta funcionando, por lo que copiamos
todos los archivos .py y el excel de optimization_problem_data.csv en la carpeta `OPTIMIZADORAPP`. Además creamos el archivo urls.py dentro de la misma carpeta.

La justificación es debido a que a que podemos importar los modulos de una forma mas sencilla, sin la necesidad de usar PATH, el archivo urls.py nos sirve para definir las urls
de la app dentro del proyecto. Notar que al momento de copiar los archivos a la carpeta `OPTIMIZADORAPP` y al importar los modulos debemos anteponer un ., esto debido a que el import
se debe hacer de desde el mismo directorio.

### 3.2 Ejecución del modelo desde ejecutar.py

Se creó un archivo llamado ejecutar.py dentro de la carpeta OPTIMIZADORAPP. Este script tiene como objetivo ejecutar el modelo principal y generar automáticamente todos los archivos de output, tales como:

Grafico.png: gráfico con las soluciones factibles.

Archivo Excel con la cantidad óptima de productos.

Archivo .lp con el modelo exportado.

Importante:
La decisión tomada fue no modificar los archivos fuente principales (descritos en la sección 2) y crear un script adicional (ejecutar.py) que ejecute el modelo y mueva/copiar los archivos generados a la carpeta de la app.

Sin embargo, no estoy completamente seguro de si este enfoque es el óptimo a futuro, ya que:

Ejecutar ejecutar.py mueve archivos desde la carpeta raíz (OR-TOOLS) a OPTIMIZADORAPP.

Esto podría generar problemas de rutas relativas al implementarlo en Django, dado que los archivos generados se crean en la raíz y luego se trasladan, lo que puede romper referencias si la estructura de carpetas cambia.

Justificación de esta decisión:
Se prefirió mantener sin modificaciones el código original de los módulos .py para no afectar su lógica interna, centralizando la ejecución en un único script (ejecutar.py) que se encarga de correr el modelo y organizar los resultados finales.

### 3.3 OPTIMIZADOR

1-En la carpeta `OPTIMIZADOR` en settings.py registramos la APP `OPTIMIZADORAPP` agregandola en INSTALLED_APPS. Esto permite que Django la reconozca y la incluya en el proyecto.
2-En la carpeta `OPTIMIZADOR` en urls.py mediante el metodo include de django.urls agregamos  path('', include('OPTIMIZADORAPP.urls')), en urlpatterns de modo de conectar las rutas de nuestro proyecto con el de la APP.
3-En la carpeta `OPTIMIZADORAPP` en urls.py agregamos lo siguiente:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.optimizar_view, name='optimizar'),
]

Lo cual nos permite definir las rutas de `OPTIMIZADORAPP`, conectarla con views.py.

## 4 Server.

1-Iniciar el server mediante python manage.py runserver en la terminal.
2-Ingresar al siguiente Link: http://127.0.0.1:8000/ 

## 5 Extras.
En Criterios de Evaluación/Buenas prácticas en Django hablan de armar teMplates, a primera instancia no los realice, sin embargo use la IA para despues hacerlos. Al final me confundio mas de lo que creía. Por lo que lo deje como estaba funcionando. Tenia problemas con la carpeta template, no sabia donde se debiar crear y al correr el server siempre me arrojaba error.
Entiendo que este es un punto importante de evaluación, perdón por no hacerlo de la forma correcta pero estaba un poco desgastado intentando saber lo básico de django en tan poco tiempo.

