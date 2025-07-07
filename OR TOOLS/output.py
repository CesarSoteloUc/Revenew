import pandas as pd

def export(modelo):
    product_data = []
    for product_id, var in modelo.x.items():
        product_data.append({
            'Producto': product_id,
            'Cantidad optima': var.solution_value()
        })
    df_products = pd.DataFrame(product_data)

    with pd.ExcelWriter("Cantidad_optima_productos.xlsx", engine="openpyxl") as writer:
        df_products.to_excel(writer, sheet_name="Cantidad", index=False)