from django.http import HttpResponse
import os
import pandas as pd
import base64
import subprocess

def optimizar_view(request):
    base_dir = os.path.dirname(__file__)
    ejecutar_path = os.path.join(base_dir, 'ejecutar.py')
    subprocess.run(['python', ejecutar_path])
    excel_path = os.path.join(base_dir, 'Cantidad_optima_productos.xlsx')
    grafico_path = os.path.join(base_dir, 'Grafico.png')
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        data = df.to_dict(orient='records')
    else:
        data = "Archivo Excel no encontrado."
    if os.path.exists(grafico_path):
        with open(grafico_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        img_html = f'<img src="data:image/png;base64,{image_data}" />'
    else:
        img_html = "<p>Gráfico no encontrado.</p>"
    html = f"""
    <html>
    <body>
    <h1>Resultados del Modelo</h1>
    <h2>Solución Óptima</h2>
    <pre>{data}</pre>
    <h2>Gráfico</h2>
    {img_html}
    </body>
    </html>
    """

    return HttpResponse(html)