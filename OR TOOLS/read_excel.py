import pandas as pd

class DataLoader:
    def __init__(self, expected_columns=None):
        self.expected_columns = expected_columns if expected_columns else []

    def leer_excel(self, path, path_json):
        try:
            if path.endswith('.csv'):
                df = pd.read_csv(path)
            else:
                xls = pd.ExcelFile(path)
                df_list = [xls.parse(sheet_name) for sheet_name in xls.sheet_names]
                df = pd.concat(df_list, ignore_index=True)
            self.validar_estructura(df)

            df.to_json(f'{path_json}optimization_problem_data.json')
            print("Se cargo el archivo correctamente.")
            return df

        except Exception as e:
            raise Exception(f"Se encontro error en el archivo {str(e)}")

    def validar_estructura(self, df):
        missing_cols = [col for col in self.expected_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Faltan columnas requeridas: {missing_cols}")
        if df.isnull().values.any():
            raise ValueError("Existen valores nulos en el archivo.")
        for col in self.expected_columns:
            if df[col].dtype not in ['int64', 'float64', 'object']:
                print(f"Columna {col} tiene tipo {df[col].dtype}")
        if 'product_id' in df.columns:
            if df['product_id'].duplicated().any():
                raise ValueError("Existen productos duplicados en la columna 'product_id'.")
