import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Crear DataFrames de ejemplo
df_clientes = pd.DataFrame({
    "ClienteID": [1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15],
    "Nombre": ["Juan", "Maria", "Carlos", "Random_1", "Juan", "Maria", "Carlos", "Random_1", "Juan", "Maria", "Carlos", "Random_1", "Random_2", "Random_3", "R4"],
    "Edad": [25, 30, 28, 12, 34, 45, 34, 34, 34, 54, 23, 23, 45, 64, 23]
})

df_pedidos = pd.DataFrame({
    "PedidoID": [101, 102, 103, 104],
    "ClienteID": [1, 2, 3, 3],
    "Producto": ["A", "B", "C", "D"]
})

df_productos = pd.DataFrame({
    "Producto": ["A", "B", "C"],
    "Descripcion": ["Producto A", "Producto B", "Producto C"],
    "Precio": [10.0, 15.20, 20.3]
})

df_facturas = pd.DataFrame({
    "FacturaID": [201, 202, 203],
    "PedidoID": [101, 102, 103],
    "Registradores": [1001, 1003, 1001],
    "Total": [10.0, 15.20, 20.3]
})

df_empleados = pd.DataFrame({
    "EmpleadoID": [1001, 1002, 1003, 1004, 1005],
    "Nombre": ["Ana", "Pedro", "Elena", "Andrea", "Laura"],
    "Rol": ["Vendedor", "Gerente", "Vendedor", "Vendedor", "Vendedor"]
})

df_vacaciones = pd.DataFrame({
    "IDEmpleado": [1001, 1002, 1001, 1003],
    "Mes_vacaciones": ['Enero', 'Mayo', 'Enero', 'Julio'],
    "Año": [2021, 2021, 2022, 2023]
})


# Almacenar DataFrames en un diccionario
dataframes = {
    "Clientes": df_clientes,
    "Pedidos": df_pedidos,
    "Productos": df_productos,
    "Facturas": df_facturas,
    "Empleados": df_empleados,
    "Vacaciones": df_vacaciones
}

# Crear un grafo dirigido para representar las relaciones
grafo_relaciones = nx.DiGraph()

# Definir función para calcular el porcentaje de similitud de los datos
def porcentaje_valores_en_comun(df1, df2, columna_df1, columna_df2):
    df1[columna_df1] = df1[columna_df1].astype(str)
    df2[columna_df2] = df2[columna_df2].astype(str)

    valores_unicos_df1 = set(df1[columna_df1])
    valores_unicos_df2 = set(df2[columna_df2])

    valores_en_comun = valores_unicos_df1.intersection(valores_unicos_df2)
    porcentaje_en_comun = len(valores_en_comun) / len(valores_unicos_df1) * 100

    return porcentaje_en_comun

# Definir una función para inferir relaciones basándose en la similitud de Jaccard
def inferir_relaciones(df1, df2, umbral_similitud=70):
    for col1 in df1.columns:
        if 'float' in str(df1[col1].dtype):
            continue
        if len(df1[col1]) == df1[col1].nunique():
            for col2 in df2.columns:
                if 'float' in str(df2[col2].dtype):
                    continue
                if porcentaje_valores_en_comun(df1, df2, col1, col2) > umbral_similitud:
                    return col1, col2
                elif porcentaje_valores_en_comun(df2, df1, col2, col1) > umbral_similitud:
                    return col2, col1
        else:
            for col2 in df2.columns:
                if 'float' in str(df2[col2].dtype):
                    continue
                if len(df2[col2]) == df2[col2].nunique():
                    if porcentaje_valores_en_comun(df1, df2, col1, col2) > umbral_similitud:
                        return col1, col2
                    elif porcentaje_valores_en_comun(df2, df1, col2, col1) > umbral_similitud:
                        return col2, col1
        return None

# Inicializar el conjunto de nombres de DataFrames relacionados
dataframes_relacionados = set()

# Iterar sobre los pares de DataFrames y buscar relaciones
for nombre_df1, df1 in dataframes.items():
    for nombre_df2, df2 in dataframes.items():
        if nombre_df1 != nombre_df2:
            relaciones = inferir_relaciones(df1, df2)
            if relaciones:
                grafo_relaciones.add_edge(nombre_df1, nombre_df2, relaciones=relaciones)
                dataframes_relacionados.add(nombre_df1)
                dataframes_relacionados.add(nombre_df2)

# Encontrar DataFrames sin relaciones y agregar nodos para ellos
dataframes_sin_relacion = set(dataframes.keys()) - dataframes_relacionados
for df in dataframes_sin_relacion:
    grafo_relaciones.add_node(df)

# Dibujar el grafo
plt.figure(figsize=(15, 6)) 
posiciones = nx.spring_layout(grafo_relaciones)
nx.draw(grafo_relaciones, posiciones, with_labels=True, font_weight='bold', node_size=1000, node_color="skyblue", font_size=10, edge_color="gray", width=2, arrowsize=15)
plt.show()